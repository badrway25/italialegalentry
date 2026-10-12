# DOCUMENT MANIFEST — fonti autoritative Italy Legal Entry™

Generato il 20 settembre 2026 · Directory ispezionata ricorsivamente: la cartella del pacchetto (fuori dal repository, in una posizione privata)
Metodo: `scripts/document_manifest.py` (SHA-256 sul file binario, estrazione testo DOCX via
OOXML e PDF via PyMuPDF, entrambe fuori dal repository).

> **I file elencati non sono nel repository e non devono esservi copiati.**
> Vedere `docs/security/CONFIDENTIAL_MATERIAL_POLICY.md`.

---

## 1. Pacchetto ricevuto il 20 settembre 2026

Sei file, nessuna sottodirectory, tutti con data di modifica 2026-09-20 14:59.

| # | File | Ext | Byte | SHA-256 | Titolo | Ver. | Data doc. |
|---|---|---|---|---|---|---|---|
| D1 | `Italy_Legal_Entry_Master_Dossier_v2_0_20-09-2026.docx` | docx | 44 372 | `2dd30a10568666789ba16e99b784b96dd94b4b666008a54733ab3d967fd2a044` | Master Dossier dell'opera e del progetto | 2.0 | 20/09/2026 |
| D2 | `Italy_Legal_Entry_Technical_Blueprint_v1_0_20-09-2026.docx` | docx | 47 765 | `10e63363e8b45f05ba46728d9c7b3f2b7c74acd7402d9d6e987d6b6a4e32d04f` | Technical Blueprint — architettura funzionale e software | 1.0 | 20/09/2026 |
| D3 | `Relazione_Tecnica_Italy_Legal_Entry_v1.docx` | docx | 41 846 | `e6c50841f12b044306bd96c4b04c8bb82f734de58d289f5033cda66630dd6aa1` | Relazione tecnica di progetto | 1.0 | 07/09/2026 |
| D4 | `Dossier_SIAE_Italy_Legal_Entry_v1.docx` | docx | 41 054 | `cccc74cd4ab616cf64176e57f28fe967cff8fb056cdf815d88f6da1ec44284b1` | Dossier descrittivo dell'opera | 1.0 | settembre 2026 |
| D5 | `Scheda_compilazione_Mod350_Italy_Legal_Entry.docx` | docx | 38 744 | `39c2f12075195f8da64b38f621c1b93c0fbd678b3a4a6a49219f78b2dd679781` | Scheda di compilazione Mod. 350 SIAE | — | 07/09/2026 (tariffa verificata) |
| D6 | `mod_350_deposito_Italy_Legal_Entry_compilato.pdf` | pdf | 376 727 | `8f8077c0e5a65878ced9047dd2bbda4b607e87cf523389594789125d03661280` | Mod. 350 — deposito opera inedita, compilato | — | firmato 19/08/2026 |

Nota tecnica: i cinque DOCX sono stati generati con `python-docx` e riportano nei metadati la data
fittizia 2013-12-23 propria del template della libreria. La data autorevole è quella **nel testo**
del documento, riportata sopra. Il PDF D6 ha quattro pagine, nessun campo modulo AcroForm: i dati
compilati fanno parte del layer testuale.

---

## 2. Classificazione e impatto

Legenda impatto: **PUB** contenuto pubblico · **PLT** funzionalità piattaforma · **SEC** sicurezza ·
**ARC** architettura · **PRIV** privacy · **DES** design · **IP** proprietà intellettuale ·
**TIME** tempistiche di pubblicazione.

| # | Riservatezza | Natura | PUB | PLT | SEC | ARC | PRIV | DES | IP | TIME |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 Master Dossier v2.0 | **RISERVATO — non destinato alla diffusione** | Opera progettuale, modello, workflow, governance, strategia di tutela | ◐ | ● | ○ | ● | ◐ | ◐ | ● | ● |
| D2 Technical Blueprint v1.0 | **RISERVATO — pre-sviluppo** | Specifica tecnica: moduli, ruoli, dati, API, Rule Engine, sicurezza, backlog | ○ | ● | ● | ● | ● | ○ | ◐ | ◐ |
| D3 Relazione Tecnica v1.0 | Riservato (governance tecnica) | Requisiti tecnici e di conformità, scheda di verifica da compilare | ○ | ◐ | ● | ● | ● | ○ | ◐ | ○ |
| D4 Dossier SIAE v1.0 | Riservato (materiale di deposito) | Descrizione dell'opera ai fini probatori | ○ | ◐ | ○ | ◐ | ○ | ○ | ● | ○ |
| D5 Scheda Mod. 350 | Riservato (contiene istruzioni su dati personali) | Guida alla compilazione del deposito | ○ | ○ | ○ | ○ | ◐ | ○ | ● | ○ |
| D6 Mod. 350 compilato | **RISERVATO + DATI PERSONALI** | Modulo di deposito firmato | ○ | ○ | ○ | ○ | ● | ○ | ● | ● |

● impatto diretto · ◐ impatto indiretto · ○ nessun impatto

---

## 3. Finalità di ciascun documento

**D1 — Master Dossier v2.0 (20/09/2026).** Cristallizza il modello integrato prima della
presentazione pubblica del 2 ottobre. Contiene la visione, il principio metodologico
(bisogno del territorio → competenze → formazione nel Paese d'origine → percorso legale → ingresso →
inclusione), il progetto pilota Veneto–Marocco, l'architettura del modello su cinque livelli, i moduli
della piattaforma, il workflow operativo in dieci passi, il modello del Forum Permanente con i cinque
assi di cooperazione, la dimensione universitaria, la replicabilità, i principi di conformità e la
strategia di tutela. **Documento di riferimento per il prodotto e per il perimetro del progetto.**

**D2 — Technical Blueprint v1.0 (20/09/2026).** Traduce il modello in specifica implementabile:
architettura logica a cinque livelli, quattordici moduli applicativi, nove ruoli con i rispettivi
vincoli di accesso, percorso persona in undici passi, percorso impresa in dieci passi, Rule Engine
versionato con la struttura di campo delle regole, undici stati del fascicolo, ventidue entità del
modello dati, relazioni chiave, prima specifica API, governance del Forum virtuale, requisiti di
sicurezza e privacy, stack tecnico proposto, backlog MVP con priorità P0/P1/P2, dieci criteri di
accettazione della prima release e sei categorie di dati da non incorporare nel codice.
**Documento di riferimento per la piattaforma autenticata.**

**D3 — Relazione Tecnica v1.0 (07/09/2026).** Descrive requisiti architetturali e di conformità con
formulazioni deontiche («dovrà»), distinguendo esplicitamente fra specifica progettuale e stato di
implementazione effettivo. Contiene la scheda di verifica tecnica §21, da compilare a cura del
referente tecnico. **Documento di riferimento per la governance tecnica e per la conformità.**

**D4 — Dossier SIAE v1.0 (settembre 2026).** Descrizione dell'opera ai fini del deposito probatorio.
Ripropone il modello in chiave descrittiva; rileva per la comprensione del perimetro e per gli
elementi distintivi rivendicati. **Materiale di tutela, non specifica tecnica.**

**D5 — Scheda Mod. 350.** Guida operativa alla compilazione del modulo SIAE, con il testo sintetico
di descrizione dell'opera. **Materiale amministrativo.**

**D6 — Mod. 350 compilato.** Modulo di deposito firmato il 19 agosto 2026, con i dati anagrafici
della depositante e l'informativa privacy SIAE. **Materiale amministrativo con dati personali: non
deve essere letto, citato o copiato oltre quanto necessario a confermare l'avvenuta compilazione.**

---

## 4. Pacchetto precedente — 17 settembre 2026 (fuori dal repository dal 21/09/2026)

Resta pienamente in vigore per il contenuto pubblico. Non è sostituito dal pacchetto del 20 settembre.

| File | Natura | Autorità |
|---|---|---|
| `ILE_Document_Implementation_FR.pdf/.txt` | Istruzioni di implementazione e testi pubblici da copiare alla lettera | **Massima** su wording pubblico, rimozioni, date di pubblicazione, form |
| `ILE_Annexe_1_Textes_Juridiques_FR.pdf/.txt` | Traduzione di cortesia dei testi giuridici | Riferimento; **non pubblicabile** (manca l'originale italiano ufficiale) |

L'Allegato 1 in **italiano** resta mancante. Gate G1 chiuso, gate G2 chiuso di conseguenza.

---

## 5. Come sono stati letti

I sei documenti sono stati letti integralmente il 20 settembre 2026:

- DOCX: estrazione OOXML di paragrafi, tabelle, intestazioni, piè di pagina e contenuti `sdt`,
  preservando i livelli di titolo;
- PDF: estrazione testuale pagina per pagina con PyMuPDF, quattro pagine;
- i dati personali presenti nell'estrazione di D6 sono stati **redatti** nella copia di lavoro subito
  dopo la verifica della loro presenza, e non sono stati trascritti in alcun file del repository.

Totale testo estratto: circa 72 000 caratteri.

---

## 6. Verifica di integrità

Per ricalcolare gli hash e confermare che i documenti non siano cambiati, sulla macchina che
custodisce il pacchetto (fuori dal repository, in una posizione privata):

```bash
python -c "
import hashlib, pathlib
for f in sorted(pathlib.Path(r'<cartella del pacchetto>').rglob('*')):
    if f.is_file():
        print(hashlib.sha256(f.read_bytes()).hexdigest(), f.name)
"
```

Se un hash differisce, il pacchetto è stato aggiornato: rileggere il documento, aggiornare questo
manifest, rivedere `REQUIREMENT_MATRIX_V2.md` e `CONFLICT_REGISTER.md` prima di implementare.
