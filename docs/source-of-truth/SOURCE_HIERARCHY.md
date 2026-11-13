# SOURCE HIERARCHY — quale documento decide cosa

Versione 1.0 · 20 settembre 2026

I documenti non si fondono indiscriminatamente. Ogni decisione ha **una** fonte che prevale, e le
altre intervengono solo se la prima tace. Questa gerarchia è vincolante: un agente che trova una
contraddizione non la risolve in silenzio, la registra in `CONFLICT_REGISTER.md`.

---

## 1. Matrice di autorità per dominio decisionale

| Dominio decisionale | Fonte che prevale | Seconda | Terza | Non decide |
|---|---|---|---|---|
| **Testo pubblico esatto** (wording, titoli, frasi prescritte) | D0a Documento di implementazione FR | — | — | D1, D2, D3, D4 |
| **Rimozioni obbligatorie** (formulazioni vietate) | D0a | — | — | tutti gli altri |
| **Pagine giuridiche** (privacy, cookie, note legali, condizioni, disclaimer) | D0b Allegato 1 in **italiano** (MANCANTE) | D0a per le istruzioni di pubblicazione | — | traduzione di cortesia FR: mai pubblicabile |
| **Date di pubblicazione e fasi** | D0a | D1 §8 (data del Forum) | — | D2, D3 |
| **Form pubblici e consensi visualizzati** | D0a | D2 §13 (requisiti privacy) | D3 §9 | — |
| **Perimetro e visione del prodotto** | **D1 Master Dossier v2.0** | D4 Dossier SIAE | D0a | — |
| **Modello del Forum Permanente** | **D1 §8** | D2 §12 (governance digitale) | D0a (evento pubblico) | — |
| **Architettura funzionale della piattaforma** | **D2 Technical Blueprint v1.0** | D1 §6 | D3 §3 | — |
| **Ruoli e controllo accessi** | **D2 §4** | D3 §4 | D1 §6 | — |
| **Rule Engine: campi, esiti, versionamento** | **D2 §7** | D3 §6 | D1 §6 | — |
| **Stati del fascicolo** | **D2 §8** | — | — | — |
| **Modello dati** | **D2 §9–10** | D3 §8 | — | — |
| **API** | **D2 §11** | — | — | — |
| **Backlog e priorità P0/P1/P2** | **D2 §16** | D2 §21 (roadmap) | — | — |
| **Criteri di accettazione della release** | **D2 §17** | D3 §20 | — | — |
| **Sicurezza applicativa e infrastrutturale** | **D3 §13** e **D2 §13**, il più rigoroso dei due | D0a | — | — |
| **Privacy, basi giuridiche, retention** | **D3 §9** e **D2 §13**, il più rigoroso dei due | D0a (testi mostrati) | — | — |
| **Hosting e localizzazione** | **D3 §10** | D2 §13 | — | — |
| **Governance tecnica, asset, continuità** | **D3 §18** | D1 §11 | — | — |
| **Multilingua e separazione contenuti/codice** | **D2 §20** | D3 §17 | — | — |
| **Proprietà intellettuale e provenienza** | **D1 §2, §12–17** | D4 | D5, D6 | — |
| **Stack tecnologico** | **Direttiva del committente: Django** | D2 §14 è una *proposta da validare* | — | — |
| **Art direction e identità visiva** | **Direttiva di rebase del committente** | D0a (vincoli istituzionali) | — | D1–D6 |

**Legenda fonti**

- **D0a** `ILE_Document_Implementation_FR` — istruzioni di implementazione, 17/09/2026 (fuori dal repository)
- **D0b** Allegato 1 «Testi legali» in **italiano** — **NON CONSEGNATO**
- **D0c** `ILE_Annexe_1_Textes_Juridiques_FR` — traduzione di cortesia, riferimento interno (fuori dal repository)
- **D1** Master Dossier v2.0, 20/09/2026
- **D2** Technical Blueprint v1.0, 20/09/2026
- **D3** Relazione Tecnica v1.0, 07/09/2026
- **D4** Dossier SIAE v1.0, 09/2026
- **D5** Scheda Mod. 350 · **D6** Mod. 350 compilato

---

## 2. Principi di risoluzione

**P1 — Il pubblico non eredita dal riservato.**
D1 e D2 sono documenti interni. Nessuna loro frase diventa copy del sito. Il sito parla solo con le
parole di D0a e con testo scritto dal team e sottoposto ai vincoli di D0a.

**P2 — Il più recente prevale sul più antico nello stesso dominio.**
D2 (20/09) prevale su D3 (07/09) dove entrambi descrivono la stessa cosa in modo incompatibile, salvo
il principio P3.

**P3 — In sicurezza e privacy prevale il controllo più rigoroso, non il più recente.**
Se D3 chiede MFA per «amministratori e operatori privilegiati» e D2 chiede MFA «per amministratori e
ruoli sensibili», si implementa l'unione dei due insiemi, non l'intersezione.

**P4 — Una proposta tecnica non è un vincolo di titolarità.**
D2 §14 dichiara espressamente che lo stack è «una proposta pragmatica e non un vincolo» e che il
referente tecnico «può confermarlo o sostituirlo motivando compatibilità, sicurezza, competenze e
costi». D2 §18 chiede esplicitamente a Badr di validare lo stack. La scelta Django è quindi una
risposta prevista dal documento, non una sua violazione. Vedere CR-01 nel registro dei conflitti.

**P5 — Il silenzio non autorizza.**
Se nessun documento prescrive un testo pubblico, il team lo scrive e lo sottopone ai vincoli di D0a
(nessuna promessa di risultato, nessuna funzione pubblica attribuita alla piattaforma, nessuna
intermediazione non autorizzata). Non si «deduce» un testo legale da un documento interno.

**P6 — Una funzione descritta in D2 ma vietata da D0a sul fronte pubblico non è cancellata: è spostata.**
Esempio: «ricerca e selezione». D0a vieta di presentare pubblicamente attività di selezione o
matching. D2 §3 prevede un workflow di selezione assegnabile **esclusivamente a soggetti
autorizzati**. La sintesi corretta è: nessuna traccia pubblica, modulo interno con attore autorizzato
sempre esplicito e audit completo. Vedere CR-03.

**P7 — Gate prima di tutto.**
Nessuna fonte può aprire un gate chiuso. Se D1 descrive le pagine legali e D0b manca, le pagine
restano bloccate. `docs/LEGAL_AND_PUBLICATION_GATES.md` resta l'autorità operativa sui gate.

---

## 3. Cosa fare davanti a un conflitto

1. Non scegliere in silenzio.
2. Aprire una riga in `CONFLICT_REGISTER.md` con: fonte A, fonte B, affermazioni in conflitto,
   impatto, interpretazione raccomandata, decisione implementativa, necessità di conferma del
   committente.
3. Implementare l'interpretazione raccomandata **solo** se è difendibile e reversibile.
4. Se non lo è, fermare quella singola funzione e proseguire con il resto.

Bloccare l'intero lavoro è ammesso solo quando nessuna interpretazione responsabile è possibile.
