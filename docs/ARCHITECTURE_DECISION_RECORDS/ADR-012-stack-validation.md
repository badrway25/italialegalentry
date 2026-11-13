# ADR-012 — Validazione dello stack tecnico rispetto al Technical Blueprint v1.0

Data: 20 settembre 2026 · Stato: **ACCETTATA** · Sostituisce: nessuna
Richiesta da: Technical Blueprint v1.0 §14 e §18 · Conflitto correlato: CR-01

---

## Contesto

Il Technical Blueprint v1.0, al §14 «Stack tecnico raccomandato — **da validare da Badr**», propone:

| Componente | Proposta del Blueprint |
|---|---|
| Frontend | Next.js / React, TypeScript |
| Backend | NestJS/Node.js TypeScript oppure FastAPI/Python, API REST versionate |
| Database | PostgreSQL |
| Cache/coda | Redis + worker queue |
| Document storage | Object storage S3-compatibile in regione UE |
| Identity | Provider OIDC/OAuth2 o servizio dedicato con MFA |
| Search | PostgreSQL full-text |
| Rule Engine | Servizio applicativo + tabelle/versioni regole, condizioni DSL/JSON |
| Infrastruttura | Container Docker, CI/CD, ambienti separati |
| Observability | Log strutturati, metriche, error tracking, alerting |
| i18n | IT/FR/AR/EN con contenuti separati dal codice |

Lo stesso §14 premette: «Lo stack seguente è una proposta pragmatica e **non un vincolo di
titolarità**. Badr può confermarlo o sostituirlo motivando compatibilità, sicurezza, competenze e
costi.» Il §18 chiede espressamente al referente tecnico la «scelta definitiva dello stack e
motivazione di eventuali modifiche», con esito **APPROVATO / DA MODIFICARE / NON IMPLEMENTABILE**.

Nel frattempo il progetto è stato realizzato su Django 5.2 LTS con PostgreSQL 17: 22 applicazioni di
dominio, 94 modelli, 44 881 righe di Python, 169 template, 1 871 test, quattro lingue con RTL reale,
CSP self-only, gate di pubblicazione e registro dei testi vincolati con verifica verbatim.

La direttiva successiva del committente è esplicita: «Project directive remains: Django-based
ecosystem» e «Do NOT rewrite the whole system in Next.js/Nest/FastAPI just because a technical
document mentions those as possible technology choices».

---

## Decisione

**Django 5.2 LTS + PostgreSQL 17, server-rendered con progressive enhancement, è confermato come
stack del progetto.**

Risposta nella forma richiesta dal Blueprint §18, voce per voce:

| Voce del Blueprint | Esito | Sostituzione e motivo |
|---|---|---|
| Frontend Next.js/React | **DA MODIFICARE** | Template Django + CSS moderno + JavaScript progressivo. Il prodotto è a prevalenza di contenuto e di form, deve funzionare senza JavaScript, deve reggere WCAG 2.2 AA e un budget LCP < 2,5 s su rete lenta. Una SPA aggiungerebbe un secondo runtime, un secondo sistema di routing, un secondo sistema di traduzione e un secondo modello di sicurezza per ottenere, su questo prodotto, un'esperienza peggiore. Misurato: Lighthouse mobile 100/100/100, LCP 1,8 s su rete lenta simulata con CPU rallentata 4×. |
| Backend NestJS o FastAPI | **DA MODIFICARE** | Django. Le ragioni sono di sicurezza e di velocità di conformità, non di preferenza: ORM con migrazioni, sistema di permessi, protezione CSRF, i18n con RTL, back-office amministrabile e sistema di form sono nativi e testati. Con NestJS o FastAPI andrebbero assemblati e mantenuti a mano, in un progetto la cui superficie di rischio è giuridica prima che tecnica. |
| API REST versionate | **DA MODIFICARE** | Le diciotto operazioni del §11 esistono come **servizi di dominio** con gli stessi nomi. Nessuna API HTTP pubblica finché non esiste un consumatore reale: una superficie non usata è solo superficie d'attacco. Quando servirà, si aggiunge `/api/v1/` sopra gli stessi servizi. Vedere CR-02. |
| PostgreSQL | **APPROVATO** | PostgreSQL 17. |
| Redis + worker queue | **DA MODIFICARE per ora** | Non necessario alla scala attuale. Le e-mail passano da `notifications.EmailOutbox`, che è già la coda. Si introdurrà quando esisteranno compiti asincroni reali. |
| Object storage S3 in UE | **APPROVATO in architettura** | `documents` usa storage privato astratto: il passaggio a S3 in regione UE è di configurazione. Subordinato a G12. |
| Provider OIDC/OAuth2 esterno | **DA MODIFICARE** | django-allauth con modulo MFA. Un provider esterno introdurrebbe un responsabile del trattamento in più e una dipendenza sulla disponibilità di terzi per l'accesso a dati personali, senza necessità dimostrata. Resta possibile aggiungere OIDC per federazioni istituzionali future. |
| PostgreSQL full-text | **APPROVATO** | |
| Rule Engine con DSL/JSON | **APPROVATO e già realizzato** | `apps/orientation/engine.py`: valutatore puro, deterministico, senza ORM, con DSL JSON (`all`, `any`, operatori `eq`/`in`/`not_in`/`is_true`/`is_false`) e validazione di integrità del ruleset. **Nessun `eval()`.** Va esteso con giurisdizione, validità temporale, fonte, versione e approvazione a quattro occhi. |
| Docker, CI/CD, ambienti separati | **APPROVATO** | `docker-compose.yml`, `config/settings/{base,dev,prod,test}`, guardie di avvio in produzione. |
| Observability | **DA COMPLETARE** | Log strutturati con request id presenti; metriche, error tracking e alerting sono requisiti di deploy. |
| i18n IT/FR/AR/EN separato dal codice | **APPROVATO** | `i18n_patterns` su quattro lingue, catalogo gettext per l'interfaccia, modelli di traduzione con stato di pubblicazione per il contenuto, registro dei testi vincolati per il testo prescritto. |
| Monorepo `apps/web`, `apps/api`, `packages/*` | **DA MODIFICARE** | Monolite modulare `apps/<dominio>`. La separazione richiesta dal Blueprint è **di dominio**, e c'è: 22 applicazioni con confini espliciti. Mapping: `packages/domain` → i modelli e i servizi di ciascuna app; `packages/rule-engine` → `apps/orientation/engine.py`; `packages/i18n` → `locale/` più i modelli di traduzione; `packages/ui` → il design system in `static/css` e `templates/components`; `packages/contracts` → `apps/integrations`; `apps/worker` → `notifications`. |

---

## Conseguenze

**Positive**
- Nessuna riscrittura: 44 881 righe di Python funzionanti, 1 871 test e l'intera conformità già
  verificata restano.
- Un solo runtime, un solo modello di sicurezza, un solo sistema di traduzione da mantenere.
- La conformità è più facile da dimostrare: ogni controllo è in un punto solo.
- Il budget di performance è già rispettato senza lavoro di ottimizzazione.

**Negative e come si affrontano**
- Un'interfaccia molto interattiva costa più lavoro che con React. Mitigazione: progressive
  enhancement mirato, e HTMX dove un aggiornamento parziale porta un beneficio reale — con la
  libreria effettivamente caricata, a differenza di oggi.
- Un futuro consumatore mobile nativo richiederebbe l'API. Mitigazione: i servizi di dominio esistono
  già con i nomi del Blueprint; aggiungere il livello HTTP è un lavoro delimitato.
- La scelta diverge da un documento del committente. Mitigazione: questa ADR è la risposta formale
  che il Blueprint §18 richiede, ed è registrata in CR-01.

**Neutre**
- PostgreSQL, Docker, DSL del Rule Engine, i18n a quattro lingue e object storage restano come
  proposti.

---

## Da rivedere se

- Nasce un consumatore reale dell'API (applicazione mobile nativa, integrazione istituzionale con
  accordo firmato).
- Compare un requisito di interattività in tempo reale che il progressive enhancement non copre.
- La titolare del progetto richiede formalmente lo stack del Blueprint: in tal caso la migrazione va
  pianificata come progetto a sé, con stima e rischi, non eseguita di iniziativa.
