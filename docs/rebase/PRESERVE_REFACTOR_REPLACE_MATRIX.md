# PRESERVE / REFACTOR / REPLACE MATRIX

Classificazione di ogni componente maggiore prima del rebase · 20 settembre 2026

| Classe | Significato |
|---|---|
| **PRESERVE** | Funziona e resta com'è. Toccarlo è un rischio senza beneficio. |
| **REFINE** | Resta, con miglioramenti localizzati. Nessun cambio di struttura. |
| **REFACTOR** | La struttura interna cambia, il comportamento esterno no. |
| **REPLACE** | Sostituito da qualcosa di diverso. |
| **REMOVE** | Eliminato. |
| **DEFER** | Rinviato a una fase successiva, con motivazione. |

---

## 1. Fondamenta e infrastruttura

| Componente | Classe | Perché |
|---|---|---|
| Django 5.2 LTS, PostgreSQL 17, monolite modulare | **PRESERVE** | Confermato contro la proposta Next.js/NestJS (CR-01). Riscriverlo distruggerebbe 45 000 righe funzionanti per un guadagno nullo sul problema reale, che è di design e di prodotto |
| Struttura `apps/<dominio>` | **PRESERVE** | Mappa pulitamente sui moduli del Blueprint |
| `config/settings/{base,dev,prod,test}` | **PRESERVE** | Separazione degli ambienti conforme a D2 §13 |
| Guardie di produzione in `prod.py` | **PRESERVE** | Si rifiuta di avviarsi senza HTTPS, HSTS e chiave robusta |
| Ordine dei middleware | **PRESERVE** | Verificato, `check --deploy` pulito |
| CSP self-only sul pubblico, rilassata solo in back-office | **PRESERVE** | Conforme; nessun tracker, nessuna risorsa esterna |
| `core.flags`, `core.gates`, `core.clock` | **PRESERVE** | Meccanismo di pubblicazione corretto; sarà esteso ai moduli nuovi |
| `core.links.public_url` | **PRESERVE** | Impedisce strutturalmente i link a pagine chiuse |
| `core.seeds`, `core.sitemaps`, `core.public_routes` | **PRESERVE** | Registri utili |
| Docker compose per il database | **REFINE** | Aggiungere un limite di connessioni sensato: la saturazione del pool ha già causato 16 errori 500 durante la QA |
| `conftest.py` di radice | **PRESERVE** | Isolamento della lingua attiva fra i test |

## 2. Contenuto e conformità

| Componente | Classe | Perché |
|---|---|---|
| `cms/locked_content.py` e il file di hash | **PRESERVE** | Garanzia contrattuale sui testi prescritti. 236 frammenti verificati verbatim da un revisore indipendente |
| `scripts/verify_locked_against_source.py` | **PRESERVE** | Prova riproducibile della conformità |
| Test sulle formulazioni vietate | **PRESERVE** | Impediscono la reintroduzione delle diciture proibite in quattro lingue |
| `cms/middleware.LegacyURLMiddleware` | **PRESERVE** | Migrazione degli URL WordPress completata e testata |
| `legal` (documenti bloccati) | **PRESERVE** | Gate G1 corretto: nessun testo giuridico inventato |
| Cataloghi gettext it/en/ar/fr | **REFINE** | 100 % di copertura; da aggiornare a ogni nuova stringa del rebase |
| Traduzioni del questionario di orientamento | **REPLACE** | Oggi inesistenti: il contenuto appare in francese su `/it/`, `/en/`, `/ar/`. Difetto CL-01, gravità alta |
| Contenuto prescritto nelle pagine | **PRESERVE** | Verbatim, non si tocca |
| Testo scritto dal team (microcopy) | **REFINE** | Revisione secondo il registro istituzionale richiesto (RB §56) |

## 3. Design system e frontend

| Componente | Classe | Perché |
|---|---|---|
| `static/css/tokens.css` | **REPLACE** | I token esistono ma esprimono un sistema senza tesi. La nuova art direction richiede un insieme nuovo, con separazione fra token pubblici e token di piattaforma (RB §17) |
| `static/css/base.css` | **REFACTOR** | Reset, focus, helper bidi e regole di stampa restano; tipografia e ritmo verticale si rifanno |
| `static/css/layout.css` | **REPLACE** | Un solo contenitore ripetuto per ogni sezione è la causa diretta del difetto D-01 |
| `static/css/components.css` (74 KB, 29 sezioni) | **REFACTOR** | Molti componenti sono corretti nel comportamento e sbagliati nell'espressione. Si conservano struttura, stati, accessibilità e comportamento RTL; si rifanno superfici, tipografia, spaziatura e colore |
| `static/css/fonts.css` e i font IBM Plex | **REPLACE** | Scelta di ripiego. Lo studio tipografico richiesto da RB §13 deve decidere famiglie latine e araba con motivazione |
| `static/img/icons.svg` | **REFINE** | Sprite SVG valido e ben fatto; il set va ridisegnato secondo la direzione scelta, restando un solo sistema |
| Regole bidi in `base.css` | **PRESERVE** | Corrette e verificate; la nuova direzione deve ereditarle |
| `static/js/main.js` | **REFINE** | JavaScript progressivo minimo, corretto. Si estende per il guscio della piattaforma |
| Attributi HTMX presenti senza libreria caricata | **REMOVE** | Attributi morti nei template |
| Template della home (`templates/pages/home/_*.html`) | **REPLACE** | Undici sezioni con lo stesso ritmo: è il difetto principale |
| Template istituzionali | **REFACTOR** | La struttura del contenuto è corretta, la composizione no |
| `templates/components/*` | **REFACTOR** | Contratti dei componenti validi; espressione da rifare |
| `templates/base.html`, header, footer | **REFACTOR** | Diventano due gusci distinti: pubblico ed editoriale, piattaforma e operativo |

## 4. Sito pubblico

| Componente | Classe | Perché |
|---|---|---|
| `pages` — home componibile e pagine istituzionali | **REFACTOR** | Il modello `HomeSection` amministrabile è una buona idea da conservare; cambiano gli archetipi e la composizione |
| `ecosystem` — quattro spazi di pubblico | **REFACTOR** | Contenuto corretto, trattamento da rifare: sono le porte dell'ecosistema, non una griglia di servizi |
| `forum` — parte pubblica | **REFINE** | Completa e conforme. L'avviso in home va riproporzionato alla sua importanza (difetto D-05) |
| `pathways`, `faq`, `glossary`, `living`, `news` | **REFACTOR** | Contenuto e modelli validi; trattamento editoriale da costruire |
| `enquiries` — form pubblici | **REFINE** | Gate G2 corretto. I sei rilievi di gravità alta del red team su form e consensi vanno lavorati |
| `partners` | **PRESERVE** | Gate G6 corretto: nessun logo senza autorizzazione scritta |
| Hero con foto di repertorio | **REPLACE** | Cliché vietato (RB §14); serve una direzione fotografica |
| Banner del Forum in home | **REPLACE** | Oggi visivamente equivalente a un avviso sui cookie |
| Sezione «che cosa fa / che cosa non fa» | **REFACTOR** | Ottimo contenuto, presentazione da costruire |

## 5. Piattaforma autenticata

| Componente | Classe | Perché |
|---|---|---|
| `accounts.User`, `PersonProfile`, `Organisation`, `Membership` | **REFINE** | Base corretta; il profilo va esteso ai campi richiesti da D2 §5.2 |
| `accounts.roles` | **REFINE** | Aggiungere sei ruoli: soggetto autorizzato, ente formativo, professionista, redattore legale, redattore di contenuti, operatore |
| Permessi a livello di oggetto | **REFACTOR** | Da estendere a fascicolo, selezione, formazione, con test dedicati (RB §61) |
| `BackofficeMFAMiddleware` | **REFINE** | Estendere ai ruoli sensibili oltre al back-office |
| `orientation/engine.py` | **PRESERVE** | Componente tecnicamente migliore del progetto. DSL sicuro, nessun `eval()`, validazione completa |
| `orientation` — modelli e ruleset | **REFACTOR** | Diventano il nucleo del Rule Engine giuridico: giurisdizione, validità temporale, fonte strutturata, workflow a quattro occhi, snapshot integrale |
| `orientation` — viste e wizard | **REFACTOR** | Buon comportamento; esperienza da ricostruire secondo RB §23 |
| `portal` — cruscotto | **REPLACE** | Griglia di riquadri vuoti; va riprogettato attorno a percorso, prossima azione, responsabilità |
| `portal` — guscio e navigazione | **REPLACE** | Riusa il mega-menu pubblico, vietato da RB §58 |
| `portal.Message`, `portal.Deadline`, `portal.PortalNotice` | **REFINE** | Entità utili; si collegheranno al fascicolo |
| `documents` | **REFINE** | Fondamenta corrette; aggiungere versioni, stati visibili, requisiti collegati, URL firmati, aggancio antivirus |
| `consents` | **PRESERVE** | Conforme al modello richiesto |
| `audit.AuditEvent` | **REFINE** | Struttura corretta; estendere la copertura e irrobustire l'append-only |
| `integrations` | **PRESERVE** | Confine inerte per costruzione, con stati espliciti. Conforme a RB §68 |
| `community` (11 modelli non esposti) | **DEFER** | Non richiesto da P0. Resta a riposo, non si estende |
| `notifications.EmailOutbox` | **REFINE** | Base corretta per le notifiche di piattaforma |

## 6. Moduli da costruire

| Componente | Classe | Priorità |
|---|---|---|
| `CaseFile`, stati, transizioni validate | **NUOVO** | P0 |
| `ChecklistItem` con attore responsabile e scadenza | **NUOVO** | P0 |
| `LegalRule` con validità, fonte, versione, approvazione | **NUOVO** | P0 |
| `CompanyNeed` gestibile, profilo professionale | **NUOVO** | P0 |
| Guscio di piattaforma consapevole del ruolo | **NUOVO** | P0 |
| Editor delle regole con diff, anteprima e approvazione | **NUOVO** | P1 |
| `AuthorizedActor`, `SelectionProcess` | **NUOVO** | P1 |
| Academy: `Course`, `Enrollment`, catalogo, progressione | **NUOVO** | P1 |
| `TrainingPlan` e skill gap | **NUOVO** | P1 |
| `PostEntryPlan` | **NUOVO** | P1 |
| Sportello digitale con escalation | **NUOVO** | P1 |
| Forum come governance: commissioni, tavoli, proposte, progetti | **NUOVO** | P1 |
| Workspace di istituzioni, università, enti formativi, professionisti | **NUOVO** | P1 |
| CRM esteso | **DEFER** | P2 |
| Integrazioni esterne | **DEFER** | P2, e solo dopo accordi reali |

## 7. Documentazione

| Documento | Classe |
|---|---|
| `docs/CURRENT_SITE_AUDIT.md`, `REQUIREMENTS_MATRIX.md`, `CONTENT_SOURCE_MAP.md` | **PRESERVE** — storia della fase 1 |
| `docs/LEGAL_AND_PUBLICATION_GATES.md` | **PRESERVE** — autorità operativa sui gate |
| `docs/ARCHITECTURE.md` e gli 11 ADR | **REFINE** — aggiungere ADR-012 sulla validazione dello stack e gli ADR del rebase |
| `docs/DESIGN_SYSTEM.md` | **REPLACE** — sostituito da `docs/design/DESIGN_SYSTEM_2026.md` |
| `docs/ACCESSIBILITY.md`, `I18N_RTL.md` | **REFINE** — aggiornare alla nuova direzione |
| `docs/SECURITY.md`, `PRIVACY_BY_DESIGN.md` | **REFINE** — integrare threat model, classificazione dati, modello permessi |
| `docs/DEPLOYMENT.md` | **REFINE** — G12 resta blocker |

---

## 8. Sintesi

| Classe | Componenti |
|---|---|
| PRESERVE | 19 |
| REFINE | 21 |
| REFACTOR | 13 |
| REPLACE | 10 |
| REMOVE | 1 |
| DEFER | 3 |
| NUOVO | 15 |

**Nessuna riscrittura totale.** Il backend, la conformità, i gate, il contenuto vincolato e la
sicurezza restano. Cambiano il linguaggio visivo, la composizione, il guscio della piattaforma e
l'ampiezza del dominio applicativo.

È la lettura corretta della richiesta: il problema non era il codice, era che il prodotto non era
ancora un prodotto e il design non era ancora un design.
