# GATE SCORECARD — modello (§71–78 della direttiva)

Un modello per gate; una copia compilata per ogni gate in `docs/design-v4/gates/GATE_<X>_<data>.md`.
Regole: **nessuna media** (§74); **l'implementatore non è il revisore** (§72); l'AFTER deve essere
«visibilmente e materialmente superiore» al BEFORE (§73), non sottile; ogni punteggio cita ciò che il
revisore ha **osservato in Chrome visibile** (§70) — un punteggio senza osservazione non vale.

---

## 0. Identità del gate

| Campo | Valore |
|---|---|
| Gate | A · B · C · D · E (una lettera) |
| Superfici | es. C: Dashboard Persona + Mes Documents |
| URL / account | `/fr/espace-reserve/mes-documents/` (8771, `qa-person`) |
| Commit sotto revisione | `<hash>` |
| Implementatore (non vota) | nome dell'agente |
| Data e ora della revisione | |

## 1. BEFORE / AFTER (§73)

| Vista | BEFORE | AFTER | Verdetto «materialmente superiore» (sì/no + una frase) |
|---|---|---|---|
| Desktop 1440 | `docs/qa/chrome/design-v4/before/05_mes_documents.png` | `docs/qa/chrome/design-v4/after/<gate>/05_mes_documents_1440.png` | |
| Tablet 768 | | | |
| Mobile 390 | | | |
| Stato interattivo (hover/focus/press/aperto) | — | una cattura per stato, con l'elemento indicato | |
| RTL (ar) | | | |
| Reduced-motion | — | cattura con la preferenza attiva: nulla invisibile | |
| Forced-colors | — | cattura: la gerarchia sopravvive | |

## 2. I ruoli (§71) — cinque firme, cinque punteggi indipendenti

| Ruolo | Cosa giudica in via primaria | Firma | Note |
|---|---|---|---|
| Creative Director | Premium Feel · Modernity · Originality · Visual Depth · coerenza con `CREATIVE_DIRECTION.md` | | |
| UX Lead | Clarity · Interaction Quality · Mobile · efficienza (§89) | | |
| Motion Lead | Motion · budget (§67) · pattern (DS §7) · reduced-motion | | |
| Frontend Lead | token (DS): nessun valore arbitrario · CSP · nessun `style=""` · prestazioni (§68) | | |
| Accessibility Reviewer | Accessibility · contrasto misurato · tastiera · screen reader · RTL · forced-colors | | |
| Red Team indipendente (§75–78) | i quattro test | | |

Ogni ruolo compila **la propria riga** della tabella di §3; i punteggi non si sommano né si mediano.
In caso di disaccordo fra ruoli su una dimensione vale il punteggio **più basso**.

## 3. Le dieci dimensioni (§74) — scala 1–5 con ancore

**Critiche** (una sola ≤ 2 → **BLOCK**): Premium Feel · Modernity · Clarity · Institutional Credibility ·
Accessibility · Mobile. **Di sostegno** (≤ 2 → al massimo CONDITIONALLY_READY, con correzione
obbligatoria prima del gate successivo): Visual Depth · Motion · Originality · Interaction Quality.

| # | Dimensione | 1 | 2 | 3 | 4 | 5 | Punteggio | Osservazione (cosa, dove, in Chrome) |
|---|---|---|---|---|---|---|---|---|
| 1 | **Premium Feel** (critica) | HTML grezzo, bordi quasi inesistenti | ordinato ma piatto: «sito Django ben ordinato» | superfici e controlli del sistema, ma dettagli non allineati (§93) | ricchezza controllata: profondità, materiale del primario, hover ovunque; 1–2 dettagli da rifinire | indistinguibile da un prodotto premium: ogni pixel allineato, ogni stato disegnato | | |
| 2 | **Modernity** (critica) | tabella + link sottolineati + serif dominante | reskin: raggi e ombre su una pagina vecchia | grammatica 2026 presente (rail, pillole, pannelli) ma incoerente | grammatica 2026 coerente su tutta la superficie | avanzata: molle, vetro sulle barre, indicatori che traslano, transizioni di pagina, tutto coerente | | |
| 3 | **Visual Depth** | tutto sullo stesso piano | ombre casuali | livelli 0–4 usati, ma senza ruolo leggibile | ogni superficie al suo livello (DS §2), ombre a due strati, vetro solo dove ammesso | idem + la luce (mesh/FOCUS) fa leggere la gerarchia da lontano | | |
| 4 | **Motion** | nessun moto o `fade-in-up` su tutto | moto isolato senza sistema | i pattern del DS ci sono, ma durate/curve arbitrarie o budget superato | 15 pattern rispettati, budget ≤ 2, reduced-motion completo, 0 layout/paint | idem + un momento firmato memorabile (porta, JourneyRail) | | |
| 5 | **Clarity** (critica) | non si capisce cosa fare | azione primaria non distinguibile | gerarchia informazione/azione presente ma con rumore | «dove sono / cosa viene dopo / chi è responsabile / cosa manca» rispondono a colpo d'occhio | idem + zero passi cognitivi inutili (§89) | | |
| 6 | **Institutional Credibility** (critica) | sembra un marketplace o un template | corretto ma anonimo | istituzionale ma editoriale | istituzionale **e** digitale: marchio, porta, registri legali dei chip, nessun dato finto | idem + nessuna riga che un giurista respingerebbe (testi bloccati, «nessun colore significa approvato») | | |
| 7 | **Originality** | template riconoscibile (shadcn/Bootstrap) | generico ben fatto | qualche elemento proprio (porta) su base generica | senza logo si riconosce ILE: porta, navy del marchio, registri, Plex/Newsreader | idem + un componente firma nuovo che nessun benchmark ha | | |
| 8 | **Interaction Quality** | hover/focus assenti o di default | stati presenti ma incoerenti | ogni elemento interattivo ha hover/focus/press, alcuni non allineati (§93) | tutti gli stati del DS §6, allineamento a 1 px, tempi giusti | idem + feedback causale (chip che cambia, riga che si stacca, molla) senza latenza | | |
| 9 | **Mobile** (critica) | tabella desktop schiacciata a 390 | scorrimento orizzontale sulle superfici principali | composizione propria ma azioni difficili da raggiungere | schede impilate, barra inferiore, azioni raggiungibili, target ≥ 44, nessuno scroll orizzontale | idem + gerarchia identica a desktop con meno passi | | |
| 10 | **Accessibility** (critica) | errori axe, focus rimosso, contrasto sotto soglia | AA solo sul testo | AA su testo e UI, ma tastiera/screen reader incompleti | WCAG 2.2 AA misurata: contrasto (peggior fondo, anche sotto il vetro), tastiera, nomi, `aria-live`, RTL, forced-colors, reduced-motion | idem + 2.4.11 (focus mai coperto), 2.5.8, alternative testuali per ogni grafica | | |

## 4. I quattro test (§75–78) — Red Team indipendente

| Test | Domanda | Risposta richiesta | Risposta | Perché, esattamente (elemento, cattura) |
|---|---|---|---|---|
| Generic AI | «Potrebbe essere scambiato per un template generico Claude/AI?» | **NO** | | |
| Editorial | «Sembra ancora principalmente una pubblicazione editoriale/legale?» (pagine operative) | **NO** | | |
| 2026 | «Nascosto il logo, competerebbe con prodotti digitali premium del 2026?» | **SÌ** | | |
| Too much | «Abbiamo aggiunto effetti inutili solo per sembrare moderni?» | **NO** (altrimenti: elenco di cosa togliere, nell'ordine di `CREATIVE_DIRECTION.md` §6.4) | | |

Una risposta sbagliata a **uno** dei quattro test = **BLOCK**, indipendentemente dai punteggi.

## 5. Verifiche binarie (tutte devono essere «sì»)

| Verifica | Sì/No | Prova |
|---|---|---|
| Nessuna formulazione vietata (`apps/cms/forbidden.py`), nessun testo bloccato alterato | | test `test_institutional` verde + diff dei template |
| Nessun `style=""`, nessuno script inline, nessun hotlink (CSP) | | grep + console Chrome senza violazioni CSP |
| Nessun valore fuori dai token (colori, raggi, ombre, durate, curve) | | `test_v4_tokens.py`, `test_design_docs.py` (§12 keyframes) |
| «Nessun colore significa mai approvato»: nessun chip `conforme` con croma, nessun verde di verdetto | | ispezione dei chip + `chips.py` |
| Nessun dato, contatore, avatar, grafico o KPI finto | | lettura del template: ogni numero ha una sorgente |
| Coordinate, «svg», «Suspendre le mouvement», etichette di debug: assenti | | grep sul DOM reso |
| Reduced-motion: pagina completa, nulla a opacità 0 | | cattura §1 |
| Contrasto sul peggior fondo (incluso sotto il vetro) ≥ 4,5 testo / ≥ 3 UI | | tabella DS §1.9 + misura sulla cattura |
| Prestazioni: JS/CSS ≤ budget, LCP < 2,5 s, CLS < 0,1, INP < 200 ms (4G simulato) | | Lighthouse/Performance, prima/dopo (§68) |
| RTL (ar) a tre larghezze senza proprietà fisiche nel CSS nuovo | | suite `test_rtl_browser` + catture |
| Demo page dei componenti coerente (§94) | | cattura della vetrina |

## 6. Esito

| Esito | Condizione |
|---|---|
| **PASS** | tutte le critiche ≥ 4, tutte le dimensioni di sostegno ≥ 3, quattro test corretti, tutte le verifiche «sì», AFTER materialmente superiore su ogni vista |
| **CONDITIONALLY_READY** | tutte le critiche ≥ 3 e nessuna ≤ 2, al massimo due dimensioni di sostegno ≤ 2, quattro test corretti, verifiche «sì»; correzioni elencate con scadenza; **nessuna propagazione** finché non diventa PASS |
| **BLOCK** | una dimensione critica ≤ 2, **oppure** un test sbagliato, **oppure** una verifica «no», **oppure** AFTER non materialmente superiore |

Esito del gate: ☐ PASS ☐ CONDITIONALLY_READY ☐ BLOCK

Correzioni richieste (numerate, ognuna con dimensione, elemento, cattura, criterio di chiusura):
1.
2.

Firma del Creative Director (esito finale, §6 della direttiva): ______ · data/ora: ______
