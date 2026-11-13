# FEATURE MATRIX — moduli, operazioni e loro stato

Versione 1.0 · 20 settembre 2026 · Fonte: Technical Blueprint v1.0 §3, §11, §16

---

## 1. I quattordici moduli del Blueprint

Aggiornato il 21 settembre 2026. La colonna «Stato» usa le cinque classificazioni richieste:
**FUNZIONANTE** (esercitato end-to-end), **GATED** (completo ma chiuso da un flag o da una fonte
mancante), **PARZIALE**, **SOLO ARCHITETTURA**, **NON IMPLEMENTATO**.

| # | Modulo | Priorità | Stato | Dove vive | Prova |
|---|---|---|---|---|---|
| 1 | Identity & Access | P0 | **FUNZIONANTE** | `apps/accounts` | 15 ruoli, incompatibilità applicata, MFA per responsabilità, revoca di sessione, instradamento per ruolo |
| 2 | Persone | P0 | **FUNZIONANTE** | `apps/accounts`, `apps/orientation` | «Ma situation» + questionario + ri-valutazione dinamica, verificati nel browser |
| 3 | Rule Engine | P0 | **FUNZIONANTE, contenuto GATED** | `apps/rules` | Motore, versioni, quattro occhi, snapshot, replay, provenienza del contenuto. **Nessuna regola in vigore**: il seed scrive candidate, e il database rifiuta una regola approvata senza approvatore registrato |
| 4 | Fascicolo digitale | P0 | **FUNZIONANTE** | `apps/cases` | Elenco, dettaglio, checklist con responsabile e fonte, transizioni, pre-valutazione |
| 5 | Academy | P1 | **FUNZIONANTE** | `apps/academy` | Catalogo, iscrizione, moduli, piano formativo |
| 6 | Imprese / B2B | P0 | **FUNZIONANTE** | `apps/companies` | Dichiarazione con verifica, fabbisogni, competenze, analisi territoriale |
| 7 | Ricerca e selezione | P1 | **FUNZIONANTE** | `apps/selection` | Attore autorizzato, mandato datato, processo, comunicazione d'identità |
| 8 | Skill Gap & Training Plan | P1 | **FUNZIONANTE** | `apps/academy` | Piano generato dallo scarto di competenze |
| 9 | Legal/Admin Journey | P0 | **FUNZIONANTE** | `apps/cases` | Le undici transizioni dichiarate, con audit |
| 10 | Post-entry & Inclusion | P1 | **PARZIALE** | `apps/cases` | Gli stati esistono e transitano; non esiste ancora contenuto proprio della fase |
| 11 | CRM | P2 | **CONFINE DEFINITO** | `apps/integrations` | Contratto di eventi in uscita, chiave API, webhook |
| 12 | Forum Permanente | P1 | **PUBBLICO FUNZIONANTE, GOVERNANCE in corso** | `apps/forum` | Superficie pubblica e iscrizione; workspace di cooperazione dietro il flag `virtual_forum`, chiuso |
| 13 | Università & Ricerca | P1 | **PARZIALE** | `apps/ecosystem` | Pagina pubblica; nessun workspace dedicato |
| 14 | Administration | P0 | **FUNZIONANTE** | `/backoffice/`, django-unfold | Console delle fasi, editor delle regole con diff e anteprima, flag con audit |

## 2. Le diciotto operazioni di dominio

Il Blueprint §11 le elenca come endpoint REST. Qui sono **servizi di dominio** con gli stessi nomi:
vedere CR-02 per la motivazione. Ogni servizio applica l'autorizzazione al proprio interno, non
nella vista: una futura API HTTP riuserebbe gli stessi controlli senza riscriverli.

| Operazione del Blueprint | Servizio di dominio | Vista collegata | Stato |
|---|---|---|---|
| `POST /auth/register` | allauth + `accounts.services.register_declared_account_type` | signup | **FATTO** |
| `POST /auth/login` | allauth | login | **FATTO** |
| `GET/PATCH /me/profile` | `accounts.services.update_profile` / `update_situation` | profilo, «Ma situation» | **FATTO** |
| `POST /assessments` | `orientation.services.start_session` | wizard | **FATTO** |
| `GET /assessments/{id}` | `cases.services.latest_assessment` | pagina di pre-valutazione | **FATTO** |
| `POST /cases` | `cases.intake.open_case_from_session` | automatica a fine questionario | **FATTO** |
| `GET/PATCH /cases/{id}` | `cases.services.case_detail`, `transition` | fascicolo | **FATTO** |
| `POST /cases/{id}/documents` | `documents.services` | caricamento per requisito | **FATTO** |
| `GET /academy/courses` | `academy.services.catalogue` | catalogo | **FATTO** |
| `POST /academy/enrollments` | `academy.services.enrol` | iscrizione | **FATTO** |
| `POST /companies/{id}/needs` | `companies.services.create_need` | fabbisogno | **FATTO** |
| `POST /selection-processes` | `selection.services.open_process` | workspace dell'attore | **FATTO** |
| `POST /training-plans` | `academy.services.create_plan` | piano formativo | **FATTO** |
| `GET/POST /forum/proposals` | `forum` governance | workspace Forum | **GATED** (`virtual_forum` chiuso) |
| `GET/POST /forum/commissions` | `forum` governance | workspace Forum | **GATED** (`virtual_forum` chiuso) |
| `GET /admin/rules` | `rules.services.rules_in_force` | editor in `/backoffice/rules/` | **FATTO** |
| `POST /admin/rules/{id}/versions` | `rules.services.new_version` | editor, con diff e anteprima | **FATTO** |
| `GET /audit` | `audit.services` | consultazione in back-office | **PARZIALE** (nessuna vista di ricerca dedicata) |

## 3. Funzionalità per ruolo

Legenda: ● **disponibile e verificata** · ◐ parziale · ○ prevista, non ancora disponibile ·
⊘ pronta ma chiusa da un gate · — non prevista per questo ruolo.

Un ● significa che la funzione è stata esercitata: da un test d'integrazione HTTP, da un test di
dominio contro il servizio reale, o nel browser. Non significa «il codice esiste».

Le colonne seguono i quindici gruppi di `accounts.roles`; `role:legal_approver` è la colonna
«Valid.» e `role:content_editor` la colonna «Redat.».

| Funzione | Persona | Impresa | Sogg. aut. | Prof. | Ente form. | Istit. | Univ. | Legal ed. | Valid. | Redat. | Oper. | Admin |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Account e profilo | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| MFA obbligatoria | — | — | ● | ● | — | — | — | ● | ● | ● | ● | ● |
| Situazione dichiarata | ● | — | — | — | — | — | — | — | — | — | — | — |
| Questionario di orientamento | ● | — | — | — | — | — | — | — | — | — | — | — |
| Esito con fonti numerate | ● | — | — | — | — | — | — | — | — | — | — | — |
| Ri-valutazione al cambio di situazione | ● | — | — | — | — | — | — | — | — | — | — | — |
| Fascicolo proprio | ● | — | — | — | — | — | — | — | — | — | — | — |
| Fascicolo assegnato | — | — | ● | ● | — | — | — | — | — | — | ● | ● |
| Checklist con responsabile | ● | — | ● | ● | — | — | — | — | — | — | ● | ● |
| Avanzare una riga che gli compete | ● | — | ● | ● | — | — | — | — | — | — | ● | ● |
| Documenti propri | ● | ● | — | — | — | — | — | — | — | — | — | ◐ |
| Documenti di un fascicolo assegnato | — | — | ● | ● | — | — | — | — | — | — | ● | ● |
| Dichiarare l'impresa (con verifica) | — | ● | — | — | — | — | — | — | — | — | — | ● |
| Fabbisogni | — | ● | ● | — | — | — | — | — | — | — | ● | ● |
| Processo di selezione | — | ◐ | ● | — | — | — | — | — | — | — | — | ● |
| Comunicazione d'identità, con decisione | ● | — | ● | — | — | — | — | — | — | — | — | ● |
| Academy: catalogo e iscrizione | ● | — | — | — | ● | — | — | — | — | — | — | ● |
| Academy: gestione corsi | — | — | — | — | ● | — | — | — | — | — | — | ● |
| Piano formativo | ● | ◐ | ● | — | ● | — | — | — | — | — | ● | ● |
| Sportello digitale | ● | ● | — | ● | — | — | — | — | — | — | ● | ● |
| Post-ingresso | ◐ | — | — | — | — | — | — | — | — | — | ◐ | ◐ |
| Forum: workspace di cooperazione | ⊘ | ⊘ | — | ⊘ | ⊘ | ⊘ | ⊘ | — | — | — | ⊘ | ⊘ |
| Progetti e indicatori di convenzione | — | — | — | — | — | ○ | ○ | — | — | — | ○ | ○ |
| Editor delle regole | — | — | — | — | — | — | — | ● | — | — | — | ◐ |
| Approvazione delle regole | — | — | — | — | — | — | — | **no** | ● | — | — | — |
| CMS e traduzioni | — | — | — | — | — | — | — | — | — | ● | — | ● |
| Tassonomie e anagrafiche | — | — | — | — | — | — | — | — | — | ● | — | ● |
| Console delle fasi, flag e gate | — | — | — | — | — | — | — | — | — | — | — | ● |
| Consultazione audit | — | — | — | — | — | — | — | — | ● | — | — | ● |
| Gestione utenti e ruoli | — | — | — | — | — | — | — | — | — | — | — | ● |

Tre righe meritano di essere lette due volte.

**«Approvazione delle regole» è un «no» esplicito per il Legal Editor.** Non è una funzione mancante:
è il vincolo. L'autore di una regola non può approvarla, e i due ruoli sono dichiarati incompatibili
sullo stesso account. Un ● in quella cella significherebbe che la revisione a quattro occhi non
esiste.

**Il fascicolo assegnato non è mai ● per lo staff o l'impresa.** Un fascicolo si raggiunge possedendolo
o tramite un'assegnazione con un estremo di autorizzazione e una data di scadenza. Essere del
back-office non è una ragione per leggere la situazione giuridica di una persona.

**Il workspace del Forum è ⊘, non ○.** È costruito e chiuso: il flag `virtual_forum` resta serrato
fino a dopo il 30 ottobre 2026. La differenza fra «non c'è» e «c'è ma non è aperto» è quella fra un
lavoro da fare e una decisione da prendere.

## 4. Che cosa deve esistere perché P0 sia dichiarabile completo

| # | Condizione | Verifica |
|---|---|---|
| 1 | Una persona completa l'orientamento in quattro lingue e ottiene un esito con motivazione e fonti | Test end-to-end × 4 lingue |
| 2 | L'esito crea un fascicolo con checklist e responsabili | Test end-to-end |
| 3 | Il fascicolo transita fra stati con validazione e audit | Test unitari sulle transizioni + test di audit |
| 4 | Una regola giuridica si crea, si manda in revisione, viene approvata da un altro utente e si attiva | Test end-to-end |
| 5 | Una valutazione usa la versione corretta della regola e ne conserva lo snapshot | Test di riproducibilità |
| 6 | Una persona carica un documento, che ha stato, requisito collegato e audit al download | Test end-to-end |
| 7 | Un'impresa crea e modifica più fabbisogni | Test end-to-end |
| 8 | Il guscio della piattaforma mostra solo i moduli autorizzati | Test per ruolo |
| 9 | Le **tredici** asserzioni di permesso della direttiva §61 passano | `tests/security/test_object_permissions.py` — passano, dopo una correzione che l'asserzione 13 ha fatto emergere |
| 10 | Tutte le pagine di piattaforma funzionano da telefono e in arabo | Test browser |

Finché tutte e dieci non passano, lo stato non può essere «release candidate».
