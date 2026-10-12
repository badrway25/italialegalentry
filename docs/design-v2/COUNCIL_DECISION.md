# DECISIONE DEL DESIGN COUNCIL V2 — 24 settembre 2026

Stato: **DECISO** · Direzione scelta: **C — Diplomazia mediterranea contemporanea**, con trapianti
obbligatori da A e da B · Sei rapporti indipendenti in `docs/design-v2/council/` · Prototipi in
`docs/design-v2/directions/` · Evidenza raccolta in Chrome 153 visibile in `directions/*/review/`.

---

## 1. Come si è arrivati qui

Tre team hanno costruito tre territori davvero diversi su HOME (hero + quattro vie + processo) e
CRUSCOTTO PERSONA, con contenuti reali, gli asset ufficiali dell'addendum (logo verbatim, porta con
fotografia del titolare, chiave, gradini) e Motion dal bundle condiviso. Sei revisori con mandati
distinti — direzione creativa, UX di piattaforma, moto + prestazioni, accessibilità + RTL, mobile +
tipografia, Red Team indipendente — hanno guardato, misurato e classificato senza vedersi.

| Revisore | 1º | 2º | 3º | Ciò che ha pesato |
|---|---|---|---|---|
| Direzione creativa | A | C | B | la porta come centro di gravità (A); C «memorabile ma vocabolario preso in prestito dai dev-tool»; B «il baseline con gusto migliore» |
| Red Team | C | A | B | C unica a passare le nove domande; A «Linear con un logo»; B «struttura per struttura, il fold respinto» |
| Moto + prestazioni | B | A | C | B 1 layout / 4 paint a riposo; A `box-shadow` pulsante (363 paint/3 s); C maree in JS su `<g>` SVG: 27 fps |
| UX di piattaforma | C | A | B | C risponde alle cinque domande nel primo schermo; rail 2.0 di A l'unico con frontiera MA→IT |
| Mobile | C | A | B | solo C tiene l'header a 56 px; nessuna sotto il 110 % di hero a 390 |
| Tipografia | B | C | A | B unico sistema autorevole (pesi ≤ 500, asse ottico, griglia 4 px, `:lang(ar)`) |
| Accessibilità + RTL | C (17) | B (16,5) | A (14) | C 9/10 in RTL con 0 proprietà fisiche non gestite; B 9/10 in accessibilità |

Punteggio 3/2/1 su sette classifiche: **C 17 · A 13 · B 12.**

Sui quattro assi che non si mediano (premium, modernità, credibilità istituzionale, UX di
piattaforma) i tre direttori che li hanno dati: A 8/8/7/8, C 8/9/6→8*/7→8*, B 7/5/8/6.
*C sale a 8 su credibilità e piattaforma nei rapporti UX e Red Team; il 6 della direzione creativa è
motivato dalla «deriva fintech» del teal, che il § 4 tratta come rischio da mitigare, non come
verdetto.

## 2. La decisione, e perché non è la più sicura

**C è la direzione.** Non perché ha più punti — perché è l'unica in cui uno sconosciuto, a cinque
secondi dal fold, capisce che si tratta di un passaggio regolare fra due sponde retto da
istituzioni; perché il suo cruscotto risponde alle cinque domande del committente nel primo schermo
a 1440 e a 390; perché tiene l'arabo meglio di tutte; perché il suo territorio (graticola, curve di
livello, la rotta Maroc → Vénétie con coordinate reali) è un sistema grafico proprio, che regge
anche senza la fotografia. Ed è la direzione con più difetti misurabili: il moto è il peggio
ingegnerizzato dei tre e la tipografia è meno disciplinata di B. Questi difetti sono **di
esecuzione** e hanno una soluzione già scritta nei prototipi concorrenti. Il contrario — prendere B
e «renderla più ricca» — sarebbe scegliere il registro respinto il 23 e sperare in un giudizio
diverso il 30. Il Red Team lo ha nominato come rischio; lo si evita nominandolo.

A non è la seconda per cortesia. La sua idea più forte — **ogni percorso converge sulla porta** —
è la migliore lettura della porta del committente, e il suo rail 2.0 è il migliore dei tre. Entrano
in C come componenti, non come clima: il cruscotto di A è già «Linear», e la home di A perde il
titolo bloccato.

## 3. Che cosa si prende da chi

| Da | Che cosa | Dove va |
|---|---|---|
| **C** (base) | canvas mezzanotte-teal per i capitoli immersivi, carta minerale per la lettura; graticola e curve di livello come sistema grafico proprietario; la rotta a sei stazioni con coordinate; la porta evoluta sul capitolo scuro con la rotta che entra dietro la soglia; carta intestata (barra istituzionale + header) con FR/IT/EN/ع; «Suspendre le mouvement»; quattro vie a zig-zag con glifi proprietari; shell di piattaforma (barra + banda del fascicolo + rail di navigazione + «Prochaine étape» per prima + inspector a destra); composizione mobile con header 56 px; `[dir="rtl"]` per ogni `translateX` | tutto |
| **A** | la porta come **hub**: nodi degli attori (persona, organismo di formazione, università · autorità competente, impresa, istituzione) sulle due sponde, linee che convergono sulla porta — fusa con la rotta di C, che diventa la linea principale della rete; **rail 2.0** con trama + glifo + numero + parola di stato per proprietario, «Vous êtes ici», frontiera MA → IT fra 05 e 06, modo verticale sotto 1024; palette comandi `Ctrl K` e rail icone comprimibile **solo per i ruoli operatore/professionista** (per la persona resta la navigazione piena) | hero, cruscotto, fascicolo, shell staff |
| **B** | **la disciplina del moto**: la chiave si rivela una volta; nessun loop su `filter`; le maree diventano ≤ 2 strati in CSS `transform` a ≥ 20 s, in pausa fuori schermo e con reduced-motion; le quattro durate e le tre curve; **il sistema tipografico**: nessun peso sopra 500 nei titoli, Newsreader con asse ottico, interlinee su griglia di 4 px, cifre tabellari su ogni numero, `:lang(ar)` con `letter-spacing: 0` su ogni etichetta maiuscola; **lo strato di onestà**: «Étape n sur 7», TERMINÉE / À VENIR in parole, `aria-current="step"`, «à titre indicatif» dove i responsabili non vengono dal Rule Engine, misuratore a cinque segmenti, `<details>` nativi per i menu, tabelle con `caption` e `scope`; la targa mono del fascicolo; il marchio su tassello avorio nelle barre scure; l'hover «la soglia si apre» sulle quattro vie; il disegno di sezione del processo come **alternativa** alla linea che sale (la linea di C «legge come un grafico di crescita», direzione creativa) | moto, tipografia, semantica, fascicolo |

## 4. Rischi nominati e mitigazioni

| Rischio | Chi lo ha visto | Mitigazione (obbligatoria) |
|---|---|---|
| Deriva fintech: teal ovunque, ~60 % di pagina scura, isoipse su pagine LEGAL | direzione creativa, Red Team | teal = territorio (linee, etichette di sponda), **un solo blu luminoso** per link/CTA/focus; al massimo un capitolo mezzanotte per pagina fuori da HOME e FORUM (principio 7); isoipse **solo** in modalità IMMERSIVE, mai su STANDARD/DENSE/LEGAL; verde solo semantico; bronzo solo per i sigilli |
| Prestazioni: maree in JS, 27 fps | moto + prestazioni | riscrittura in CSS `transform` (≤ 2 strati, ≥ 20 s, lineare), `IntersectionObserver` per la pausa, stato fermo con reduced-motion; verifica in Chrome Performance: 0 layout / 0 paint a riposo |
| Fotografia da 949 KB come LCP | tutti | derivati AVIF/WebP responsive dal master del titolare, ≤ 120 KB per viewport, poster con `fetchpriority="high"` |
| Hero > 110 % del viewport a 390 | mobile | composizione mobile propria: porta ridotta e a destra del titolo o sopra a 40 vh, CTA in vista senza scroll |
| Sbordo a 1024 (nav collassa solo ≤ 900) | mobile | cassetto fino a 1279 px come nel sito attuale (breakpoint di navigazione 80rem) |
| Contenuti: responsabili per tappa inventati, «0 en retard» inventato, frase informativa della pre-valutazione persa, «la plateforme» come responsabile | UX di piattaforma | i responsabili vengono da `cases.services` / Rule Engine o sono «à titre indicatif» in chiaro; nessun numero che il modello non calcola; la frase «Prochaines étapes à caractère informatif…» torna; «la plateforme» non è mai un responsabile |
| Titolo bloccato retrocesso (A) | direzione creativa | «ITALY LEGAL ENTRY™» è l'H1 dell'hero, trattamento di C (serif 300, grande); «Le parcours régulier…» è il lead |
| Didascalia inglese su pagina francese (A, B) | Red Team | «Une porte, pas un raccourci» (C) — tradotta in IT/EN/AR con revisione madrelingua per l'arabo |
| Lock-up compresso (rapporto marchio/wordmark 1,9 → 2,1–2,7) | mobile + tipografia | il lock-up scala come **unità** 38/20/8,5; sotto la soglia in cui non entra, solo il marchio |
| `.state--pending` 3,2:1, isoipse invisibili in forced-colors, «ع» < 24 px, checklist senza `caption` | accessibilità | tutti nel must-fix, con i riferimenti del rapporto |
| Fascicolo non prototipato da nessuno | UX di piattaforma | il fascicolo è il primo schermo della vertical slice dopo home e cruscotto: FONDEMENT, cambio di stato, intervenants, «Faire évoluer l'état» entrano nel disegno, non nel retrofit |

## 5. Ciò che resta umano

Sessione reale con NVDA/JAWS/VoiceOver; Windows High Contrast reale; revisione araba madrelingua
(bidirezionalità, numerali, Naskh a 12–100 px, la didascalia); dispositivi reali iOS/Android;
il master della fotografia dal titolare. Restano `HUMAN_QA_REQUIRED` nel rapporto finale.

## 6. Come si procede

1. **Fase 6 — `DESIGN_SYSTEM_V2.md`** dalla decisione: token (colore, superfici a sette livelli,
   tipografia, spazio, moto), componenti pubblici e di piattaforma, modalità di pagina.
2. **Fase 7 — architettura**: `static/css/v2/` che sostituisce `register.css` invece di sommarsi;
   `static/js/src/` per le firme (porta, rotta, rail, header); CSP invariata; nessuna isola React
   finché non si giustifica per iscritto.
3. **Fase 8–14 — vertical slice** in Django, in questo ordine e ognuna vista in Chrome prima della
   successiva: HOME (hero con porta + rete, quattro vie, processo) → NAV pubblica → LOGIN →
   CRUSCOTTO PERSONA → FASCICOLO. Poi il Council rivede la slice; solo dopo si propaga.
4. Ogni schermo: 1440 / 768 / 390 / 320, AR, reduced-motion, tastiera, Performance panel; commit
   `design-v2:` per schermo.
