# DIREZIONE C — EURO-MEDITERRANEA / DIPLOMAZIA CONTEMPORANEA

Design Council V2 · ITALY LEGAL ENTRY™ · 23 settembre 2026
Prototipo: `home.html`, `dashboard.html`, `styles.css`, `main.js`, `shots/` (tutto in questa cartella).
Servito su `http://127.0.0.1:8790/docs/design-v2/directions/c-contemporary-diplomacy/home.html`.

## 1. Concetto in dieci righe

1. La piattaforma è una **cooperazione fra due rive**: la Vénétie e il Marocco non sono una mappa con confini ma due rilievi disegnati a curve di livello, uniti da una rotta.
2. Il canvas è **minerale e notturno**: grigio minerale caldo per i capitoli di lettura, mezzanotte con sottotono teal per i capitoli immersivi (hero, processo, barra della piattaforma).
3. Il **verde italiano è semantico** (regolare, approvato, terminato), mai marca; il **bronzo desaturato** vale solo per i segni a sigillo (autorità, giurisdizione, jeu de règles).
4. Un solo accento interattivo: il **teal mediterraneo** (#0F6A72 su chiaro, #7FD1D8 su scuro) per link, CTA e focus.
5. Il sistema grafico è **cartografico**: graticola, tacche di coordinate, isoipse, plumb-line; coordinate reali (33.97° N · 6.85° W / 45.41° N · 11.88° E) come firma testuale, mai bandiere, aerei, valigie.
6. La **porta** del committente (arco + fotografia + chiave + tre gradini) è il passaggio fra le due rive: la rotta entra dietro la soglia e riemerge oltre la volta.
7. Il **letterhead**: barra istituzionale e header su carta minerale con il lock-up ufficiale intatto; sotto, il territorio notturno.
8. Tipografia a tre voci: **grotesk umanista** (Fira Sans) per l'interfaccia, **serif display ad alto contrasto** (Newsreader 300) per i titoli, **mono** (Fira Mono) per riferimenti, coordinate e folio; compagni arabi dichiarati.
9. Il moto è **territoriale**: linee che si tracciano e si posano, una marea lenta e sospendibile, sezioni che arrivano come documenti posati su un tavolo, la rotta del processo che si disegna con lo scroll.
10. Personalità: **autorità diplomatica + calore + memorabilità** — un'organizzazione internazionale del 2026, non un ministero, non una startup.

## 2. Palette come token CSS, con i rapporti di contrasto calcolati

Calcolo WCAG 2.x (luminanza relativa, script `c_contrast.py`). Soglie: testo ≥ 4.5:1, componenti UI e grafica ≥ 3:1.

```css
:root {
  /* Capitolo mezzanotte (sottotono teal) — scala di profondità */
  --mid-0: #0A151C;  --mid-1: #0E1B23;  --mid-2: #14242E;  --mid-3: #1B2F3A;  --mid-4: #223A46;
  --hairline-dark: rgba(214,226,228,.14);  --hairline-dark-strong: rgba(214,226,228,.28);
  --on-dark: #EEF2F1;  --on-dark-2: #B7C3C4;  --on-dark-3: #8FA0A3;
  --teal-300: #7FD1D8;  --teal-400: #3FA6AF;  --green-300: #7CCFA0;  --bronze-300: #C7A77E;
  /* Capitolo minerale */
  --min-0: #F4F3F0;  --min-1: #ECEBE6;  --min-2: #FBFAF8;  --min-3: #FFFFFF;
  --hairline: #D3D2CC;  --hairline-strong: #7A868B;
  --ink: #15222A;  --ink-2: #4A5A62;  --ink-3: #55646B;
  --teal-700: #0F6A72;  --teal-500: #1D8A93;  --teal-100: #D9EEF0;
  --green-700: #1E7A4D;  --green-100: #DCEFE4;  --bronze-600: #8C6D4B;  --bronze-100: #EFE6DA;
  --error-700: #B3261E;  --error-100: #F6DEDC;
  /* Marca ufficiale — mai alterata */
  --brand-green: #157A3C;  --brand-navy: #0F2547;  --brand-red: #C4142B;  --brand-gold: #C39A2B;
  /* Scala delle quattro vie (mai da sola: indice + glifo + testo) */
  --route-1: #0F6A72;  --route-2: #1C5F7C;  --route-3: #34506A;  --route-4: #2F6B5C;
  /* Responsabili (rail 2.0) */
  --owner-person: #0F6A72;  --owner-platform: #34506A;  --owner-training: #1C5F7C;  --owner-authority: #8C6D4B;
}
```

| Token | Hex | Su | Hex | Ruolo | Rapporto | AA |
|---|---|---|---|---|---|---|
| `--on-dark` | #EEF2F1 | `--mid-1` | #0E1B23 | testo | 15.51:1 | ✓ |
| `--on-dark-2` | #B7C3C4 | `--mid-1` | #0E1B23 | testo | 9.68:1 | ✓ |
| `--on-dark-3` | #8FA0A3 | `--mid-1` | #0E1B23 | testo (folio, didascalia porta) | 6.44:1 | ✓ |
| `--on-dark` | #EEF2F1 | `--mid-3` | #1B2F3A | testo | 12.29:1 | ✓ |
| `--on-dark-2` | #B7C3C4 | `--mid-3` | #1B2F3A | testo | 7.67:1 | ✓ |
| `--teal-300` | #7FD1D8 | `--mid-1` | #0E1B23 | link/accento | 10.01:1 | ✓ |
| `--teal-300` | #7FD1D8 | `--mid-3` | #1B2F3A | link/accento | 7.93:1 | ✓ |
| `--teal-400` | #3FA6AF | `--mid-1` | #0E1B23 | UI (isoipse, tacche) | 6.07:1 | ✓ |
| `--green-300` | #7CCFA0 | `--mid-1` | #0E1B23 | semantico "terminata" | 9.41:1 | ✓ |
| `--bronze-300` | #C7A77E | `--mid-1` | #0E1B23 | sigillo | 7.72:1 | ✓ |
| `--mid-1` | #0E1B23 | `--teal-300` | #7FD1D8 | testo bottone primario (scuro) | 10.01:1 | ✓ |
| `--ink` | #15222A | `--min-0` | #F4F3F0 | testo | 14.62:1 | ✓ |
| `--ink-2` | #4A5A62 | `--min-0` | #F4F3F0 | testo secondario | 6.46:1 | ✓ |
| `--ink-3` | #55646B | `--min-0` | #F4F3F0 | testo terziario (folio) | 5.48:1 | ✓ |
| `--ink` | #15222A | `--min-2` | #FBFAF8 | testo su foglio | 15.56:1 | ✓ |
| `--ink-2` | #4A5A62 | `--min-1` | #ECEBE6 | testo su area | 6.00:1 | ✓ |
| `--teal-700` | #0F6A72 | `--min-0` | #F4F3F0 | link/CTA | 5.69:1 | ✓ |
| `--teal-700` | #0F6A72 | `--min-2` | #FBFAF8 | link su foglio | 6.05:1 | ✓ |
| `--teal-500` | #1D8A93 | `--min-0` | #F4F3F0 | anello di focus / bordo UI | 3.70:1 | ✓ (UI) |
| `--green-700` | #1E7A4D | `--min-0` | #F4F3F0 | semantico | 4.80:1 | ✓ |
| `--bronze-600` | #8C6D4B | `--min-0` | #F4F3F0 | sigillo (icona) | 4.30:1 | ✓ (UI) |
| `--error-700` | #B3261E | `--min-0` | #F4F3F0 | errore | 5.89:1 | ✓ |
| `--min-0` | #F4F3F0 | `--teal-700` | #0F6A72 | testo bottone primario (chiaro) | 5.69:1 | ✓ |
| `--hairline-strong` | #7A868B | `--min-0` | #F4F3F0 | bordo di componenti | 3.37:1 | ✓ (UI) |
| `--hairline` | #D3D2CC | `--min-0` | #F4F3F0 | filetto (informativo) | 1.51:1 | — |
| `--brand-green` | #157A3C | `--min-2` (header) | #FBFAF8 | wordmark ITALY | 5.19:1 | ✓ |
| `--brand-red` | #C4142B | `--min-2` (header) | #FBFAF8 | wordmark ENTRY | 5.78:1 | ✓ |
| `--brand-navy` | #0F2547 | `--min-2` (header) | #FBFAF8 | wordmark LEGAL | 14.63:1 | ✓ |
| `--brand-green` | #157A3C | `--mid-1` | #0E1B23 | wordmark su scuro | 3.23:1 | ✗ → variante |
| `--brand-red` | #C4142B | `--mid-1` | #0E1B23 | wordmark su scuro | 2.90:1 | ✗ → variante |
| `--brand-gold` | #C39A2B | `--brand-navy` | #0F2547 | chiave nell'arco (decorativa) | 5.80:1 | ✓ |
| `--route-1…4` | vedi sopra | `--min-2` | #FBFAF8 | indici delle vie | 6.05 / 6.76 / 8.05 / 5.96 | ✓ |

Le due righe in rosso sono la ragione tecnica della variante scura del lock-up (§ 13).

## 3. Tipografia

Prototipata con le famiglie locali di `/static/css/fonts.css`:

| Voce | Famiglia | Pesi/usi | Compagno arabo |
|---|---|---|---|
| Display / titoli | **Newsreader** (variabile 200–800, `font-optical-sizing: auto`) | 300 per il display (52→100 px, interlinea 0.98, tracking −0.015em), 400 per i titoli di sezione (32→48), corsivo 400 per il lead dell'hero; 600 solo nel wordmark ufficiale | **Noto Naskh Arabic** 400–700 |
| Interfaccia / testo | **Fira Sans** (umanista) | 400 corpo 17 px, 500 UI, 600 solo per etichette maiuscole spaziate (link-arrow, stazioni) | **IBM Plex Sans Arabic** 400/500/600 |
| Riferimenti / coordinate / folio | **Fira Mono** | 12–13 px, tracking .06–.10em, cifre tabellari (`tnum`) per dossier, date, coordinate | numerali occidentali in tutte le lingue (coerenza dei riferimenti di pratica) |

Scala: 100/48/32/22/20/17/15/14/13/12 px; interlinee multiple di 4; 75 caratteri massimi per riga (`.measure`, `max-inline-size` sui paragrafi).
Regole: nessun 700 nei titoli; tracking negativo solo ≥ 40 px e 0 in arabo; `text-transform: uppercase` solo su folio/eyebrow/stazioni e sui testi bloccati già maiuscoli (le quattro vie).

**Proposta per la produzione** (da licenziare, non prototipata): *Neue Frutiger + Neue Frutiger Arabic* (Monotype, "same tone of voice regardless of the language") come grotesk umanista con eredità wayfinding = percorso; *Signifier* o *Rhymes Display* Light come serif display ad alto contrasto; *IBM Plex Mono* per i dati. Newsreader + Fira restano un fallback OFL credibile.

## 4. Scala di profondità (sette livelli)

| Livello | Minerale (chiaro) | Mezzanotte (scuro) | Materiale |
|---|---|---|---|
| 0 canvas | `--min-0` #F4F3F0 | `--mid-1` #0E1B23 (`--mid-0` per utility/footer) | nessuna ombra |
| 1 area / editoriale | `--min-1` #ECEBE6 (utility bar, area rail) | `--mid-2` #14242E (case band, pilot card, focus card) | hairline 1 px |
| 2 interattivo (foglio, pannello via, riga) | `--min-2` #FBFAF8 + hairline | `--mid-3` #1B2F3A + hairline-dark | `--shadow-2` solo in hover; il pannello via "si solleva" 2 px con la linea d'ormeggio che si traccia |
| 3 elevato (focus card, popover, menu) | `--min-3` bianco | `--mid-4` #223A46 | `--shadow-3` key+ambient |
| 4 focus | anello 2 px `--teal-500` + alone 5 px al 30 % | anello `--teal-300` + alone | offset 2 px, mai coperto dall'header sticky (`scroll-padding-block-start`) |
| 5 overlay (drawer di navigazione, modali) | `--min-2` | `--mid-2` | `--shadow-5` + scrim |
| 6 immersivo (hero, porta) | — | fotografia dentro l'arco, vignetta radiale, `backdrop-filter` **solo** sull'header scrollato (barra fluttuante) | ombra 64 px sotto l'arco |

`grep box-shadow styles.css` restituisce solo i ruoli 2/3/5 e le due ombre della porta; `backdrop-filter` compare una volta sola (header `.is-scrolled`, disattivato sotto 900 px).

## 5. Vocabolario del moto

Curve: **una d'ingresso** `cubic-bezier(.25,1,.5,1)` (easeOutQuart), **una d'uscita** `cubic-bezier(.7,0,.3,1)`, **una standard** `cubic-bezier(.4,0,.2,1)`. Durate: 120 / 180 / 240 / 320 ms; 600–900 ms solo nel capitolo immersivo (tracciati); loop ambientali 28 / 34 / 40 s (marea) e 12 s (chiave, andata e ritorno). Nessun overshoot. Solo `transform`, `opacity`, `stroke-dashoffset`. Ogni animazione passa per `withMotion(fn, settle)`: il ramo `settle` produce lo stesso stato finale.

| Nome | Funzione | Innesco | Cosa si muove | Durata / curva | Moto ridotto |
|---|---|---|---|---|---|
| Titolo riga per riga | gerarchia | load | le due righe del titolo escono da una maschera (`translateY 110% → 0`) | 600 ms, easeOut, stagger 80 ms | visibile subito |
| Il territorio si traccia | orientamento | load | rotta hero `stroke-dashoffset 1 → 0` (`pathLength=1`), stazioni `scale .4 → 1` | 900 ms + 240 ms stagger 120 | disegnato, stazioni ferme |
| Marea | profondità | load; pausa fuori viewport e a tab nascosto | tre strati di isoipse traslano ±12/9/6 px (parallasse di profondità) | 28/34/40 s lineare, alternato | fermo; il bottone «Suspendre le mouvement» scompare perché non ha lavoro |
| La porta si apre | percorso → connessione → avanzamento | load | l'arco si traccia (900 ms), i tre gradini si posano dal più largo (`scaleX`, stagger 100 ms); **arco interno e chiave sono visibili dal primo paint** (mai opacità 0): la chiave si assesta di 8 px (500 ms) poi respira (±6 px, 6 s a/r) su un involucro HTML, con un alone pre-renderizzato in opacità/scala (nessun `filter` in loop) | 0.15 → 1.4 s | tutto completo e fermo, alone al 70 % |
| Fotografia | profondità | scroll (ScrollTimeline via `scroll()`) | l'immagine dentro l'arco scorre di 18 px sull'intero hero | lineare | ferma |
| Documenti posati sul tavolo | gerarchia / causalità | `inView` all'88 % | ogni foglio/pannello arriva da 10 px **sopra** a 101.2 % e si posa (`opacity`, `y`, `scale`); fratelli in stagger 60 ms | 320 ms easeOut | visibile |
| Rotta del processo | causalità | scroll-linked (`scroll()` sull'intera sezione, 85 % → 70 %) | `stroke-dashoffset` della rotta fra le due rive | lineare con lo scroll | disegnata |
| Marcatore «étape actuelle» | stato | load (dashboard) | `scale .5 → 1`, opacità | 240 ms easeOut | visibile |
| Hover pannello via | feedback | pointer/focus-within | `translateY −2 px`, ombra ruolo 2, linea d'ormeggio `scaleY 0 → 1`, isoipse del pannello da 30 % a 50 % | 240 ms | — |
| Hover porta | feedback | pointer | l'insieme sale 4 px, l'arco interno 3 px, il primo gradino diventa oro | 320 ms easeOut | — |
| Header scrollato | orientamento | sentinella IntersectionObserver | carta all'88 % + blur, ombra ruolo 2 | 240 ms | istantaneo |

Azioni ripetute da tastiera (menu, tab, rail di navigazione) non animano.

## 6. Le quattro componenti firma

**(a) Hero — il territorio e la porta.** Capitolo mezzanotte a tutta altezza: graticola 160 px con tacche, tre strati di isoipse generati in modo deterministico (`c_territory.py`, seed fisso, nessun `Math.random`) con due rilievi — nord in alto a destra, sud in basso a sinistra — assottigliati da una maschera ellittica sotto il testo; una rotta con sei stazioni che parte dalla riva sud, **entra dietro la soglia della porta** (stazione 4 a filo della spalla sinistra) e **riemerge oltre la volta** (stazioni 5–6). Colonna sinistra: eyebrow mono, `ITALY LEGAL ENTRY™` verbatim (Newsreader 300, 100 px, `dir="ltr"`, `translate="no"`), lead corsivo bloccato, corpo bloccato, due CTA. Colonna destra: la porta (§ 13). Striscia di chiusura: coordinate delle due rive e il controllo della marea. Nessun oggetto inventato: la data del Forum (testo bloccato p2.home.banner) vive ora nella testata delle quattro vie come scheda «En ce moment».

**(b) Le quattro vie — un molo di quattro pontili.** Griglia 12 colonne a zig-zag (7/5 · 5/7) invece di quattro card uguali: ogni pannello è un foglio di livello 2 con indice serif, etichetta mono, glifo isoipsa proprio (picco singolo / doppio picco / terrazze / cresta), titolo e bottone bloccati, e una **linea d'ormeggio** sul bordo iniziale che si traccia in hover/focus; una scala teal→ardesia per via, mai da sola. Sotto 1024 px 6/6, sotto 720 px lista verticale.

**(c) Il processo — la rotta fra due rive.** Capitolo mezzanotte. SVG 1200×340 con graticola, due rive (isoipse clip-pate agli angoli), sei nodi su sei colonne (100·300·…·1100) e plumb-line che scendono al bordo; sotto, un `<ol>` di sei stazioni allineate alle stesse colonne (BESOIN → COMPÉTENCES → FORMATION → PARCOURS RÉGULIER → ENTRÉE → INCLUSION), ognuna con numero, etichetta, una riga di testo e il **responsabile** con glifo (impresa, persona, formazione, autorità a sigillo bronzo, territorio). I nodi delle autorità hanno l'anello bronzo. Il testo bloccato `p3.persons.how_it_works` è la didascalia; il progetto pilota (titolo e sequenza bloccati, otto tappe) è una scheda a lato, mai presentato come canale autorizzato. Sotto 1024 px lo SVG sparisce e le stazioni diventano tre colonne con dorsale, sotto 720 una lista verticale. In RTL lo SVG è specchiato (`scaleX(-1)`), le etichette sono HTML e non si specchiano.

**(d) Rail giurisdizione/responsabilità 2.0.** `<ol>` di sette segmenti (le sette tappe del cruscotto), ciascuno con barra di 10 px in **texture per responsabile** (pieno = persona, hachures 45° = équipe du projet, punti = organisme de formation, linee = autorité compétente), stato (`data-state` done/current/upcoming: pieno / bordo teal 2 px + marcatore / attenuato), numero, etichetta, responsabile con glifo, tag «Étape actuelle» (`aria-current="step"`), legenda testuale. Multi-attore possibile con due texture affiancate. Sotto 720 px passa in **modalità verticale**: barra di 10 px a lato, marcatore a metà altezza, etichette a destra. Mai solo colore: texture + glifo + testo + testo nascosto «Terminée.» per lo screen reader. Il mapping responsabile→tappa è illustrativo: in produzione arriva dai servizi dei casi, non dal template.

## 7. Shell della piattaforma — «la scrivania»

Non sidebar+topbar generici ma tre regioni: (1) **barra della piattaforma** (56 px, mezzanotte) con il lock-up in variante scura, il contesto `E46E03B461` in mono e le azioni; (2) **case band** (livello 1 mezzanotte con la banda territoriale al margine finale): breadcrumb, `Tableau de bord`, riferimento in teal, quattro fatti (objectif, état come pillola con glifo ✓, responsable, avancement con misuratore a cinque tacche = conteggio, non percentuale); (3) **spazio di lavoro** 224 / 1fr / 320: rail di navigazione appiccicoso con glifi a tratto 1.5 e nota legale, colonna centrale con **prochaine étape** (un solo foglio, bordo teal, responsabile a sigillo, «Cette étape ne dépend pas de vous»), rail 2.0, checklist (élément · état · responsable · échéance, con note del responsabile e «Aucune échéance» per lo screen reader), documenti (mono, tipo, stato «Non analysé» con glifo), e un **inspector** appiccicoso: pré-évaluation («Parcours pertinent», jeu de règles v1 · 21.09.2026 con sigillo bronzo e la nota che non è una decisione), messaggi e scadenze vuoti con il **glifo arco+gradini** (la grammatica della porta, senza copiarla), account. Piè di pagina a due righe.

## 8. Composizione mobile (390 / 320)

- Header 56 px: marchio ufficiale (38 px) + wordmark 14 px + tagline **8.5 px** (mai ridotta; misurata 8.5 px a 1440 e a 390) + «Menu»; sotto 360 px resta il solo marchio; drawer a schermo intero su carta con le voci a 52 px e la CTA in fondo; Escape chiude, il focus torna al bottone.
- Hero: **la porta viene prima** (220 px, ridotta ma intera: arco, foto, chiave, gradini, didascalia), poi eyebrow, titolo a 52 px, lead, corpo, CTA a tutta larghezza sotto 400 px; striscia delle coordinate a due colonne con il controllo della marea a piena larghezza. La graticola diventa texture (slice).
- Vie: lista verticale, isoipsa ridotta a 200×150, target ≥ 44 px.
- Processo: stazioni in lista verticale con dorsale a sinistra.
- Cruscotto: barra con marchio a tessera + azioni a icona (lingua «FR»), case band a colonna singola, rail di navigazione come striscia orizzontale scorrevole (36 px, bordo teal per la pagina corrente), rail 2.0 verticale, checklist come schede impilate con etichette `data-label`, inspector in coda.
- Nessuno scroll orizzontale a 320 (verificato); gutter 16 px.

## 9. Note RTL / arabo

Questa direzione nasce per essere forte in arabo: la rotta si legge da destra, la porta è a sinistra, i rilievi si specchiano.
- Solo proprietà logiche in tutto il CSS nuovo (`inset-inline-*`, `margin-inline-*`, `padding-inline-*`, `border-inline-start`); nessun `left/right`.
- `[dir="rtl"]`: gli SVG decorativi (territorio, banda del cruscotto, rotta del processo, isoipse dei pannelli) sono specchiati con `scaleX(-1)`; le frecce hanno `icon--flip-rtl`; la freccia di link-arrow in hover trasla nel verso di lettura; il marcatore del rail e le linee d'ormeggio usano `inset-inline-start`.
- **Non** si specchiano: il lock-up (`direction: ltr`), il titolo bloccato (`dir="ltr"`), i numeri, la chiave e la fotografia.
- `:lang(ar)`: IBM Plex Sans Arabic per l'interfaccia, Noto Naskh Arabic per display e titoli; `letter-spacing: 0` ovunque; `text-transform: none`; interlinea 1.8 nel corpo, 1.2–1.35 nei titoli (segni diacritici); nessuna opacità sul testo; `min-inline-size: 120px` sui bottoni; numerali occidentali coerenti per i riferimenti di pratica.
- Prototipo: `?dir=rtl` imposta `dir="rtl" lang="ar"` per verificare la composizione (le stringhe restano francesi; gli screenshot `*_rtl_*` lo mostrano).

## 10. Rischi

1. **Peso della fotografia**: l'originale del committente è 2400 px / 950 KB. In produzione servono varianti AVIF/WebP 480/800/1200 (≤ 120 KB), `<picture>` con `sizes`, e il poster per LCP.
2. **Bilanciamento porta / titolo**: due firme forti nello stesso hero. Il rischio è che la porta «vinca» sul titolo bloccato: mitigato con la colonna 7/5, il titolo a 100 px, la porta allineata in basso. Da riverificare con i testi IT/EN/AR.
3. **Tricolore nel letterhead vs. direzione senza bandiere**: il lock-up ufficiale porta verde/rosso; il resto della pagina non li usa mai. La coerenza regge finché il verde resta semantico e il rosso solo errore.
4. **Due chapter scuri per pagina** (hero + processo): il principio 7 prevede al massimo un capitolo inchiostro; qui l'hero è immersivo e il processo un secondo capitolo. Se la revisione lo giudica troppo, il processo può passare su `--min-1` con lo SVG in teal-700 senza perdere il disegno.
5. **Nav a otto voci + lock-up**: a 1024–1240 px il tagline sparisce e il wordmark scende a 17 px; sotto 900 drawer. Una settima voce in più non ci starebbe.
6. **Mapping responsabile→tappa**: illustrativo, deve venire dai servizi (Rule Engine / cases) e non dal template.
7. **Il loop della chiave dura 12 s** (a/r), sotto i 20 s dei loop ambientali del moodboard: è l'unico oggetto vivo del committente; sospeso con la marea, fermo in moto ridotto.
8. **Layer di isoipse**: ~43 KB di SVG inline nell'hero; generato a build time, cacheabile; da misurare INP/LCP su 4G simulato.

## 11. Candidati 21st.dev esaminati (ricerca via MCP, nessuna generazione)

**Hero** (query «institutional dark hero animated lines map topographic», «hero section serif typography editorial dark elegant»):

| Nome | URL | Preso come ispirazione |
|---|---|---|
| Luminous Topography (@rmahammad) | https://21st.dev/@rmahammad/components/luminous-topography | **Studiato col codice**: geometria deterministica (PRNG seed, Catmull-Rom → cubiche), maschera ellittica «safe area» sotto il testo, strati con parallasse di profondità, pausa fuori viewport e a tab nascosto, `forced-colors` con `CanvasText`. Ripreso in Python a build time; scartati la luce che segue il cursore e il `drop-shadow` sui tratti luminosi (filtro costoso). |
| Topo Field (@mengto) | https://21st.dev/@mengto/components/topo-field | contro-riferimento: WebGL in iframe, fuori budget e fuori CSP |
| Shader Hero (@beratberkayg) | https://21st.dev/@beratberkayg/components/shader-hero | contro-riferimento: shader = «catalogo 21st» |
| Hero Section Dark (@kinfe123) | https://21st.dev/@kinfe123/components/hero-section-dark | griglia sottile su scuro con titolo grande; scartato il glow |
| Halide Topo Hero (@shivendra9795kumar) | https://21st.dev/@shivendra9795kumar/components/halide-topo-hero | strati topografici in parallasse; scartata la grana 3D |
| Animated Hero Section / Roadmap (@ravikatiyar162) | https://21st.dev/@ravikatiyar162/components/animated-hero-section-2 | tappe su un sentiero rivelate allo scroll → rotta con stazioni |
| Expanded Map (@dev.shejanmahamud) | https://21st.dev/@dev.shejanmahamud/components/expanded-map | contro-riferimento: mappa letterale con tile — vietata |
| Constellation Field / Starfield / Black Hole (@mengto, @nexus-ui, @yura) | https://21st.dev/@mengto/components/constellation-field | contro-riferimenti: particelle e canvas |
| Editorial Image Hero / Editorial Hero (@felipemenezes098) | https://21st.dev/@felipemenezes098/components/hero-07 · /hero-05 | tagline a sinistra, titolo serif, asimmetria; presi il ritmo eyebrow→titolo→lead |
| Classy Hero (@jatin-yadav05) | https://21st.dev/@jatin-yadav05/components/classy-hero | tipografia elegante su scuro; scartato lo sfondo animato |

**Navigazione** (query «navbar header scroll morphing mega menu premium»):

| Nome | URL | Preso come ispirazione |
|---|---|---|
| Morphing Scroll Navbar (@laziekiki) | https://21st.dev/@laziekiki/components/morphing-scroll-navbar | **Studiato col codice**: stato «floating» oltre la soglia con `backdrop-filter` e hairline, `aria-current="location"`, rAF sullo scroll. Preso: header che cambia stato allo scroll (qui via sentinella IntersectionObserver, senza listener di scroll). Scartati: capsula che si restringe, barra di progresso, curve con overshoot `(.34,1.32,.5,1)`. |
| Navbar Section 2 (@solaceui) | https://21st.dev/@solaceui/components/navbar-section-2 | barra scura + hero chiaro: contro-esempio per il nostro letterhead chiaro + hero scuro |
| Motion Navigation Menu (@unlumen) | https://21st.dev/@unlumen/components/motion-navigation-menu | pillola attiva con layout animation; ripresa come sottolineatura 1 px che si traccia |
| Header 1 / Header 3 (@efferd) | https://21st.dev/@efferd/components/header-1 · /header-3 | drawer mobile con blur; preso il drawer a tutta altezza, scartato il blur su mobile |
| Scroll Navigation Menu (@spaceboydavey) | https://21st.dev/@spaceboydavey/components/scroll-navigation-menu | contro-riferimento: hamburger fluttuante su desktop |
| Liquid Morph Floating Menu (@aayush-duhan) | https://21st.dev/@aayush-duhan/components/liquid-morph-floating-menu | contro-riferimento: organico/ludico |
| Navbar Menu (@manuarora700), Mega Menu (@ln-dev7), Navbar (@geekles007), Navbar 1 (@preetsuthar17) | https://21st.dev/@manuarora700/components/navbar-menu … | mega-menu e hover: nessuna gerarchia da prendere per otto voci piatte |

**Processo** (query «process timeline steps scroll progress path svg»):

| Nome | URL | Preso |
|---|---|---|
| Svg follow scroll (@reuno-ui) | https://21st.dev/@reuno-ui/components/svg-follow-scroll | **Studiato col codice**: `pathLength` + `strokeDashoffset` legati a `scrollYProgress`. Ripreso con Motion `scroll(animate(path,{strokeDashoffset:[1,0]}))` su ScrollTimeline; scartata la sezione da 350 vh. |
| Product Timeline (@hyperiux) | https://21st.dev/@hyperiux/components/timeline | contro-riferimento: Lenis + GSAP orizzontale |
| Process Timeline (@shadcnui-blocks/timeline-05) | https://21st.dev/@shadcnui-blocks/components/timeline-05 | verticale con check: ripreso solo nella modalità mobile delle stazioni |
| Growth Story Timeline (@shadcnspace) | https://21st.dev/@shadcnspace/components/timeline-01 | linea che si riempie allo scroll |
| Processing Timeline (@rmahammad) | https://21st.dev/@rmahammad/components/processing-timeline | stato per tappa + responsabile → colonna «responsable» del rail |
| Text Along Path / Marquee Along SVG Path (@danielpetho) | https://21st.dev/@danielpetho/components/text-along-path | contro-riferimento: testo lungo la curva è decorativo |

`get_component` usato tre volte (Luminous Topography, Morphing Scroll Navbar, Svg follow scroll), solo per studio di struttura; nessun codice importato; nessuna generazione.

## 12. UI-UX-Pro-Max (v2.13.0) — cosa ho consultato e cosa ho fatto

| Query | Dominio | Risposta | Verdetto |
|---|---|---|---|
| diplomatic institutional midnight teal cartographic | color | «Research Lab: navy #1E3A5F + accent #A16207 + bg #F8FAFC», «Real Estate: teal #0F766E», «Translator: blue #2563EB» | **Respinto** in blocco: navy-slate freddo e accent bronzo saturi; presa solo la conferma che teal + navy scuro leggono «fiducia». Palette costruita e verificata da noi (§ 2). |
| humanist grotesk high contrast serif display institutional | typography | Playfair/Source Serif/JetBrains, Space Grotesk bold-only, Inter+Playfair | **Respinto**: Playfair e Inter sono negli anti-pattern; accolta l'idea del tri-stack sans/serif/mono con mono per etichette e date. |
| multi-step process visualization route responsibility | ux | «Step 2 of 4 indicator», WCAG redundant entry, `text-wrap: balance` sui titoli corti | **Accolto**: «Étape 2 sur 7» nel rail; `text-wrap` non usato (titolo bloccato spezzato a mano in due righe mascherate). |
| line drawing svg path reveal scroll ambient reduced motion | gsap | scroll reveal 300–400 ms power1.out y 12; stagger ≤ 8; scrub/pin | **Accolto** come baseline (320 ms, y 10, stagger 60 ms, ≤ 7 fratelli); **respinto** il pinning. |
| international organization premium dark institutional | style | «Dark Mode OLED #000», skeuomorfismo, cyberpunk | **Respinto**: nero puro e neon sono l'opposto della scala di superfici; conferma indiretta che il buio non è di per sé premium. |

## 13. Asset ufficiali (addendum del committente)

### 13.1 Il logo — lock-up ufficiale, non ridisegnato

- **File**: `/static/brand/original/logo-mark.svg` (viewBox 0 0 200 200) usato come `<img>` a 38×38 px: nessuna ridefinizione della geometria, dei colori o delle proporzioni; nessun effetto (nemmeno lo shimmer della chiave e la rotazione in hover del sito attuale: era una curva con overshoot e un `filter` in loop). In hover il marchio sale di 1 px.
- **Lock-up** identico all'originale: marchio + 12 px + wordmark serif (Newsreader 600, 20 px, `.13em`, maiuscolo, ITALY verde #157A3C · LEGAL navy #0F2547 · ENTRY rosso #C4142B) + tagline «Digital Pathways to Italy» (Fira Sans 8.5 px, `.22em`, grigio). `.lock` ha `direction: ltr`: non si specchia in arabo.
- **Dove e come respira**: header pubblico su carta minerale (`--min-2`) con hairline — la barra istituzionale sopra è anch'essa su carta (`--min-1`), così il **letterhead** è tutto chiaro e il territorio scuro comincia sotto; header scrollato: carta all'88 % + blur, il lock-up non cambia; 1024–1240 px: tagline nascosta e wordmark a 17 px; ≤ 720 px wordmark 14 px con tagline a 8.5 px; ≤ 360 px solo il marchio (38 px) con `aria-label`; footer (scuro): variante scura; barra della piattaforma (scura, 56 px): variante scura senza tagline; ≤ 720 px solo il marchio a tessera.
- **Variante scura, perché serve**: su `--mid-1` il verde è 3.23:1 e il rosso 2.90:1 (§ 2), sotto la soglia per un testo di 15–20 px. Invece di ricolorare la marca, il **marchio resta identico su una tessera di carta** (`--min-0`, 46 px, raggio 6, padding 4) e il **wordmark diventa monocromo** (`--on-dark`, stessa serif, stesso tracking). È l'unica variante e vive solo su superfici scure.
- **Cosa non ho fatto**: nessuna versione «outline», nessun gradiente, nessuna animazione del marchio, nessun uso dei due piani verde/rosso come motivo decorativo altrove.

### 13.2 La porta — l'«arch-photo-bg» evoluto, non sostituito

Letti `portal.html`, `portal.css`, `reveal.js` e gli screenshot `legacy_arch_*`. Tenuti: **la geometria dell'arco** (aspect 3/4, `border-radius 190px 190px 0 0`, bordo hairline, arco interno offset `::before` a 16 px), **la fotografia del committente** dentro l'arco (`/docs/design-v2/brand-original/arch-photo-original-2400.jpg`, `object-fit: cover`), **l'arco interno navy #0F2547** (52 % di larghezza, aspect 1/1.55, raggio 110), **la chiave** (SVG verbatim, 34 % dell'arco interno, oro #C39A2B), **i tre gradini** 66/80/94 %, **la didascalia** «A doorway, not a shortcut» — resa come testo reale in francese («Une porte, pas un raccourci», mono 10 px `.2em`) sotto la porta, perché rafforza il messaggio anti-frode.

Evoluzione nel linguaggio di questa direzione:
- **Passaggio fra due rive**: la porta occupa la colonna destra dell'hero (5/12, max 380 px, allineata in basso); la rotta del territorio **entra dietro la soglia** e **riemerge oltre la volta** verso la riva nord; la graticola e le isoipse le convergono attorno.
- **Sul buio**: l'arco non è più sabbia→carta ma `--mid-3`→`--mid-1`; la fotografia sale a opacità .50 (.62 in hover) con saturazione .8 perché su mezzanotte l'originale a .28 sparirebbe; la vignetta radiale è mezzanotte (non navy) con un velo teal in alto; l'arco interno ha un filetto interno teal al 18 % e un'ombra profonda; i gradini sono teal-300 in tre opacità, il primo diventa oro in hover.
- **Tracciato**: un SVG a parte (`.doorway__trace`, `preserveAspectRatio="none"`, `vector-effect: non-scaling-stroke`) ridisegna il profilo dell'arco con `pathLength=1` e si traccia in 900 ms al caricamento.
- **Coreografia** (§ 5): arco → gradini (dal più largo) → assestamento della chiave; **arco interno (navy pieno #0F2547) e chiave sono visibili dal primo paint** in ogni stato (normale, dopo il reveal, moto ridotto): misurati 66.8 × 144.8 px a 1440 (34.0 % dell'arco interno di 196.5 px, come l'originale) e 38.5 × 83.5 px a 390. Poi la chiave respira 6 s a/r (solo `translateY` su un involucro HTML, l'SVG resta intatto) con un **alone pre-renderizzato** (`radial-gradient` oro, alfa ≤ .26, opacità .45–.9) al posto del `drop-shadow` animato: contrasto oro/navy 5.80:1 sul navy pieno e ≈ 4.4:1 nel punto più chiaro dell'alone; la fotografia scorre di 18 px con lo scroll dell'hero. In hover: l'insieme sale 4 px, l'arco interno 3 px.
- **Mobile**: la porta viene prima del titolo, intera, a 220 px (300 px fino a 1024).
- **Moto ridotto**: tutto completo e fermo (arco tracciato, gradini posati, chiave e alone al 70 %).
- **Accessibilità**: il blocco è `aria-hidden`; la didascalia è testo reale; l'immagine ha `alt=""`.

**Cosa è cambiato rispetto all'originale**: eliminati `cubic-bezier(.34,1.56,.64,1)` (overshoot), `portalInnerFloat` (l'arco interno è fermo: il moto sta nella chiave), `keyGlow`/`keyInfiniteLevitate` con `filter` (sostituiti da alone in opacità e traslazione), la rotazione della chiave in hover, `.rv` con `transitionDelay` inline (vietato dal CSP: qui `withMotion` + classi); l'immagine Unsplash sostituita dalla fotografia del committente; posizionamenti con `translateX(-50%)` sostituiti da `inset-inline-start` (Motion possiede la `transform`, e in RTL non serve specchiare).

**Nel cruscotto**: nessuna porta. Solo la grammatica: il marchio a tessera nella barra, il glifo arco+gradini negli stati vuoti (messaggi, scadenze), il misuratore a tacche nel case band.

## 14. File, verifica, screenshot

- `home.html` (hero + quattro vie + processo + footer), `dashboard.html` (shell + case band + prochaine étape + rail 2.0 + checklist + documenti + inspector), `styles.css` (token, sette livelli, componenti, responsive 1240/1024/900/720/400, RTL, forced-colors), `main.js` (moduli ES; `import { animate, scroll, inView, stagger, withMotion } from "/static/js/dist/motion.js"`).
- CSP: zero `style=` e zero `<style>`; un solo `<script type="module" src="main.js">` per pagina; nessuna risorsa esterna; font da `/static/css/fonts.css`; SVG del territorio generati a build time (`c_territory.py` + `c_inject.py` nello scratchpad) e inlineati.
- Self-check Playwright/Chromium headless (`c_check.py`): home e dashboard a **1440×900, 390×844, 768×1024, 320×640**, più varianti **RTL** (desktop, mobile) e **reduced-motion** (desktop): **0 errori di console, 0 richieste fallite, 0 overflow orizzontale** in tutte le 14 combinazioni.
- Screenshot in `shots/`: `doorway_1440_firstpaint.png` / `_settled.png`, `doorway_390_*.png`, `doorway_1440_reduced_*.png` (element screenshot della porta nei tre stati), `home_desktop_fold.png`, `home_desktop_full.png`, `home_mobile_fold.png`, `home_mobile_full.png`, `home_tablet_*.png`, `home_narrow_*.png`, `home_desktop_rtl_*.png`, `home_mobile_rtl_*.png`, `home_desktop_reduced_*.png`, e gli equivalenti `dashboard_*`.
