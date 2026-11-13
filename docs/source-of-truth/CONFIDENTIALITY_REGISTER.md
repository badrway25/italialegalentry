# CONFIDENTIALITY REGISTER

Versione 1.0 · 20 settembre 2026 · Policy operativa: `docs/security/CONFIDENTIAL_MATERIAL_POLICY.md`

Classificazione di ogni fonte e di ogni categoria di materiale derivato.

Livelli: **P** pubblico · **I** interno (team di progetto) · **R** riservato (accesso nominativo,
NDA richiesto) · **R+PD** riservato con dati personali (minimizzazione e accesso eccezionale).

---

## 1. Documenti sorgente

| Doc | Marcatura nel documento | Livello | Nel repository | Pubblicabile | Note |
|---|---|---|---|---|---|
| D1 Master Dossier v2.0 | «RISERVATO — NON DESTINATO ALLA DIFFUSIONE» | **R** | NO | mai | Opera oggetto di deposito SIAE; la pubblicazione ne comprometterebbe il carattere inedito |
| D2 Technical Blueprint v1.0 | «SPECIFICA TECNICA RISERVATA — PRE-SVILUPPO» | **R** | NO | mai | Contiene Rule Engine, modello dati e architettura di sicurezza |
| D3 Relazione Tecnica v1.0 | non marcato, natura interna | **R** | NO | mai | Requisiti di sicurezza e governance |
| D4 Dossier SIAE v1.0 | materiale di deposito | **R** | NO | mai | Descrizione dell'opera a fini probatori |
| D5 Scheda Mod. 350 | materiale amministrativo | **R** | NO | mai | Contiene istruzioni su dati anagrafici |
| D6 Mod. 350 compilato | modulo firmato | **R+PD** | NO | mai | Codice fiscale, data e luogo di nascita, residenza, cellulare, e-mail privata |
| D0a Documento di implementazione FR | istruzioni di pubblicazione | **I** | **NO — rimosso dal repository e dalla cronologia il 21/09/2026** | i testi prescritti sì, il documento no | I testi marcati «À INSÉRER» sono destinati al pubblico; il documento che li contiene no |
| D0c Allegato 1 FR (cortesia) | traduzione non ufficiale | **I** | **NO — rimosso dal repository e dalla cronologia il 21/09/2026** | **no** | Gate G1: manca l'originale italiano |
| D0b Allegato 1 **IT** ufficiale | — | — | **NON CONSEGNATO** | sarà pubblico | Blocca G1 e G2 |

---

## 2. Materiale derivato

| Categoria | Livello | Dove | Regola |
|---|---|---|---|
| Identificatori di requisito (`REQ-…`) | **I** | `docs/source-of-truth/` | Citabili in commit, test, issue |
| Manifest con SHA-256 e metadati | **I** | `docs/source-of-truth/DOCUMENT_MANIFEST.md` | Nessun contenuto riservato |
| Documentazione di piattaforma derivata | **I** | `docs/platform/` | Parafrasi tecnica, non riproduzione della forma espressiva |
| Threat model, classificazione dati, modello permessi | **I** | `docs/security/` | Mai esposti da una vista pubblica né in documentazione API pubblica |
| Condizioni delle regole giuridiche | **I** | database + back-office | La logica dettagliata non compare su pagine pubbliche |
| Schema del database, migrazioni | **I** | repository | Mai in pagine pubbliche |
| ADR | **I** | `docs/ARCHITECTURE_DECISION_RECORDS/` | Decisioni tecniche, nessun contenuto riservato del dossier |
| Testi prescritti pubblici | **P** | `apps/cms/locked_content.py` | Copia verbatim dei testi «À INSÉRER» |
| Estrazioni testuali dei documenti riservati | **R** | fuori dal repository, in una posizione privata | Da cancellare a fine lavorazione |
| Screenshot di QA dell'area autenticata | **I** | `docs/qa/` (PNG non versionati) | Solo account sintetici; nessun dato reale |
| Dati di seed e fixture | **P/I** | `apps/*/seeds.py` | Solo dati sintetici; nessun nome di persona reale |

---

## 3. Dati personali presenti nelle fonti

| Fonte | Categoria | Tipo | Trattamento adottato |
|---|---|---|---|
| D6 | Depositante (persona fisica) | Codice fiscale, data e luogo di nascita, indirizzo di residenza, cellulare, e-mail professionale, firma | Letto una sola volta per confermare la natura del documento; **redatto** nell'estrazione di lavoro; mai trascritto nel repository |
| D1, D4, D5 | Titolare e referente tecnico | Nome e cognome, ruolo | Mai sul sito pubblico (CR-06); citabili solo in documentazione interna dove necessario |
| D0a | Funzioni istituzionali | Nessun nome, solo cariche | Le cariche sono pubblicabili; i nomi restano bloccati dal gate G5 |

Nessun dato personale proveniente da queste fonti entra nel database applicativo, nei seed, nelle
fixture di test o nei log.

---

## 4. Controlli

- `tests/security/test_confidential_material.py` — cerca nel repository versionato: gli hash dei sei
  documenti, i loro nomi di file, le marcature «RISERVATO — NON DESTINATO ALLA DIFFUSIONE» e
  «SPECIFICA TECNICA RISERVATA» e i riferimenti pubblici del modulo di deposito. Gli identificativi
  privati del depositante non sono nel repository: il test li legge da una tabella privata indicata
  da `ILE_CONFIDENTIAL_SENTINELS` e, dove la variabile manca, lo dichiara con un test saltato.
- `tests/compliance/test_no_person_names.py` — verifica che nessun nome di persona fisica compaia
  nelle pagine pubbliche renderizzate, nei seed, nei cataloghi di traduzione e nei metadati.
- `.gitignore` — `*.docx`, `mod_350*`, `*RISERVATO*`, `docs/source-of-truth/_raw/`.

---

## 5. Ciclo di vita

| Evento | Azione |
|---|---|
| Nuovo documento ricevuto | Aggiornare manifest, registro, gerarchia delle fonti e matrice dei requisiti prima di implementare |
| Deposito SIAE effettuato | Annotare la data; il carattere «inedito» cessa con la divulgazione pubblica del 2 ottobre |
| Accordo di sviluppo e riservatezza firmato | Registrarne l'esistenza qui, senza allegarlo |
| Fine lavorazione | Cancellare le estrazioni testuali di lavoro (fuori dal repository, in una posizione privata); i documenti originali restano presso la titolare |
| Repository reso pubblico | Verificare preventivamente con i test di cui al §4 e con una revisione manuale di `docs/` |
