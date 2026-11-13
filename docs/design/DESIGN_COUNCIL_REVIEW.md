# DESIGN COUNCIL REVIEW — critiche indipendenti della build respinta

20 settembre 2026 · Dieci specialisti in sola lettura, una lente ciascuno, nessuna conclusione
suggerita · Prove: 272 screenshot in `docs/qa/visual/before/`, misurazioni dal vivo con Playwright,
lettura del codice

---

## 1. Esito complessivo

| Lente | Punteggio | Rilievi |
|---|---|---|
| Accessibilità (WCAG 2.2 AA) | 5,5/10 | 16 |
| Architettura dell'informazione | 4/10 | 13 |
| Identità visiva | 4/10 | 15 |
| Tipografia | 4/10 | 11 |
| Art direction | 4/10 | 14 |
| Responsive e motion | 4/10 | 14 |
| UX pubblica | 4/10 | 16 |
| RTL e arabo | 3,5/10 | 12 |
| Direzione editoriale e fotografica | 3/10 | 12 |
| UX della piattaforma | 3/10 | 13 |
| **Media** | **3,9/10** | **136** |

Gravità: **32 critici**, 51 alti, 44 medi, 9 bassi.

Nessuna lente ha superato 5,5. Il committente aveva ragione, e la concordanza fra dieci esperti che
non si sono parlati è essa stessa il dato più significativo.

---

## 2. I dieci problemi ricorrenti

Questi sono emersi **indipendentemente da più lenti**. Sono i problemi veri, distinti dalle opinioni
singole raccolte al §3.

### R-01 — Una sola larghezza di contenitore, per sempre
*Rilevato da: art direction, tipografia, identità visiva, responsive*

Misurato dal vivo: a 1440 px tutte e sette le fasce della home riportano larghezza interna 1200 px a
x=120. A 1920 px tutte e sette riportano 1200 px a x=360: il 37,5 % dello schermo diventa margine.
La causa è `--container-max: 75rem` applicato senza condizioni; `--container-wide` esiste e non è
usato per nulla di strutturale.

Conseguenza: una pagina le cui fasce hanno tutte lo stesso bordo non può avere una gerarchia di
momenti, non può produrre una composizione asimmetrica e non può sembrare scritta da qualcuno.

### R-02 — Ogni sezione pesa uguale
*Rilevato da: art direction, tipografia, identità visiva*

Stili calcolati a 1440: le cinque sezioni di contenuto della home rendono l'occhiello a 12 px con
spaziatura 1,44 px, il titolo a 33,76 px con interlinea 38,82, il lancio a 21 px, larghezza 576 px.
Non simili: **identici a due decimali**. La spaziatura verticale è 72/72 px su ognuna.

È letteralmente il pattern «eyebrow + H2 + paragraph» che il committente ha vietato. Quando ogni
sezione si annuncia allo stesso modo, il lettore non ha nulla da ordinare.

### R-03 — L'hero non è un hero
*Rilevato da: art direction, tipografia, editoriale*

L'H1 è 48 px contro un H2 di 33,76: rapporto 1,42. Il token `--font-size-display` non è usato dalla
home. La fotografia misura 484×363 px, il 34 % della larghezza, ed è una riunione generica attorno a
un tavolo di legno, riusata identica su un'altra pagina.

### R-04 — Le quattro entrate, che sono la promessa del prodotto, sono sepolte
*Rilevato da: UX pubblica, architettura dell'informazione, responsive, UX di piattaforma*

La home dichiara «Quattro accessi all'ecosistema… ogni attore dispone del suo spazio». A 390 px le
quattro entrate cominciano rispettivamente a 1,82, 2,29, 2,76 e 3,23 schermate di scorrimento. In
Fase 1 due delle quattro non hanno né navigazione né pagina.

Una promessa che il visitatore deve cercare per tre schermate non è una promessa.

### R-05 — L'arabo è francese specchiato, non un prodotto
*Rilevato da: RTL e arabo, tipografia, UX pubblica*

L'**ingegneria** RTL è eccellente: zero overflow su 25 pagine arabe, specchiatura corretta,
catalogo dell'interfaccia tradotto al 100 %. Il **prodotto** arabo non esiste: una pagina araba tipica
è araba al 44 % dei caratteri; il sistema di design contiene una sostituzione di font e otto regole.
Non c'è una coppia display/testo per l'arabo come esiste per il latino.

### R-06 — La piattaforma è una pagina pubblica con una barra laterale
*Rilevato da: UX di piattaforma, architettura dell'informazione, identità visiva*

L'area autenticata fallisce tutte e quattro le domande di accettazione poste dal committente: chi
entra non vede dove si trova, qual è il suo percorso, che cosa fare adesso, chi è responsabile. I
cruscotti della persona e dell'impresa sono, pixel per pixel, lo stesso schermo.

### R-07 — La scala tipografica è schiacciata e il serif non lavora
*Rilevato da: tipografia, art direction, identità visiva*

Tre gradini reali in cima alla scala; otto token compressi in una banda di 9 px sotto i 24 px, quattro
dei quali con valori duplicati. Il serif compone fra il 4 % e il 19 % delle parole: decora i titoli,
non porta la lettura. Ventidue titoli in maiuscolo forzato con spaziature arbitrarie. Misure di lettura
fino a 147 caratteri.

### R-08 — Nessun linguaggio grafico proprio
*Rilevato da: art direction, identità visiva, editoriale*

Tolte la fotografia e il logotipo non resta nulla di riconoscibile. Il bronzo fa otto lavori diversi
(38 dichiarazioni in `components.css`) e quindi non significa niente.

### R-09 — La fotografia non è governata come contenuto
*Rilevato da: editoriale, art direction*

La **governance** delle immagini è ottima: registro delle licenze, hosting locale, formati moderni.
La **direzione** non esiste: sei fotografie di repertorio servono 52 pagine, nessuna ha didascalia,
nessuna ha credito, cinque proporzioni diverse ritagliano al centro la stessa libreria 3:2.
Lo stile `<figcaption>` esiste in `base.css` e non è mai stato usato.

### R-10 — Il mobile è un riflusso, non una composizione
*Rilevato da: responsive e motion, UX pubblica, accessibilità*

Una sola composizione autorizzata a cadere. Su telefono la home è alta quasi 9 000 px. Peggio: su
telefono e tablet del contenuto **scompare senza JavaScript**, e il linguaggio di movimento è un
insieme di effetti hover che su un dispositivo touch non esiste.

---

## 3. Osservazioni di una sola lente, comunque da trattare

Non sono meno vere: sono semplicemente emerse da un solo punto di vista.

| # | Osservazione | Lente |
|---|---|---|
| S-01 | Il wizard di orientamento perde le risposte e il fuoco a ogni passo | accessibilità |
| S-02 | Il comando di chiusura del menu mobile sta sotto il proprio pannello | accessibilità |
| S-03 | L'altezza della testata appiccicata è scritta da JavaScript su un elemento di cui i fratelli hanno bisogno | accessibilità |
| S-04 | «Forum» nomina tre cose diverse nell'interfaccia | architettura dell'informazione |
| S-05 | Il metodo del progetto (bisogno → competenze → formazione → percorso → ingresso → inclusione) non ha un URL | architettura dell'informazione |
| S-06 | Il marchio è un logotipo senza segno | identità visiva |
| S-07 | `--font-mono` è dichiarato e mai caricato | tipografia |
| S-08 | L'azione primaria di un flusso cambia rango fra le superfici: pulsante pieno in home, contorno nel portale | art direction |
| S-09 | Gli URL non sono localizzati: una pagina araba è servita su un percorso francese | RTL e arabo |
| S-10 | Nessun foglio di stile per la stampa, benché una pre-valutazione stampata sia un uso reale del prodotto | responsive |

---

## 4. Che cosa il Council ha difeso

Una critica che non distingue ciò che funziona non è utilizzabile. Tutti e dieci hanno segnalato
elementi da **non** distruggere:

- **L'indice numerato dei percorsi regolari** (01–08): ordinale bronzo, titolo serif, glossa sans,
  filetto, freccia. È l'unico oggetto genuinamente editoriale del sito e ha il registro di un
  registro giuridico. Va promosso a pattern portante, non lasciato dentro una sezione.
- **L'hero del Forum**: l'unica fascia a piena larghezza e l'unico momento con presenza. Dimostra
  che la squadra sa farlo; lo fa una volta sola.
- **La sezione «che cosa fa / che cosa non fa»**: l'unica con un'idea compositiva, due colonne in
  opposizione. È anche l'argomento istituzionale più importante del sito.
- **L'assenza dei difetti grossolani**: raggi 2–3–4 px, cinque sole ombre sull'intera home, nessun
  gradiente, nessun glassmorphism, nessun contatore, nessuna emoji, nulla centrato, ogni titolo in
  `text-align: start` così l'arabo si specchia correttamente.
- **L'ingegneria RTL**: zero overflow su 50 misurazioni, proprietà logiche ovunque.
- **I token di colore con annotazioni di contrasto reali** e la parità d'inchiostro latino/arabo
  misurata al 3 %.
- **`docs/IMAGE_LICENSES.md`** e la disciplina di hosting locale.
- **Il pattern `layout-sidebar`**, già usato su 22 template: la struttura esiste, manca l'uso
  compositivo.

---

## 5. La frase che riassume le dieci critiche

> L'esecuzione è competente. L'intenzione manca.

Nessuna lente ha trovato lavoro sciatto. Tutte hanno trovato lavoro **non deciso**: un sistema che
applica correttamente regole che nessuno ha scelto.

---

## 6. Che cosa ne è seguito

1. Tre direzioni artistiche complete, strutturalmente diverse (`ART_DIRECTION_A/B/C.md`).
2. Quattro giudici indipendenti, con mandati diversi, che le hanno valutate su dieci criteri.
3. Una decisione motivata con innesti nominati (`ART_DIRECTION_DECISION.md`).
4. Un sistema di design nuovo (`DESIGN_SYSTEM_2026.md`) e archetipi di pagina
   (`PAGE_ARCHETYPES.md`) prima di toccare una sola pagina.

I 136 rilievi sono tracciati come lavoro, non archiviati come opinioni.
