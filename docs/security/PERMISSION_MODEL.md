# PERMISSION MODEL — Italy Legal Entry™

Versione 1.0 · 20 settembre 2026 · Requisiti: **REQ-IAM-04…10**, **REQ-SEC-01**
Owner: referente tecnico · Revisione: **obbligatoria a ogni nuovo ruolo, a ogni nuovo modello di dominio**

Documenti correlati: `docs/source-of-truth/PLATFORM_REQUIREMENTS_V2.md` §2 e §20 ·
`docs/source-of-truth/CONFLICT_REGISTER.md` (CR-03, CR-04, CR-09, CR-10) ·
`docs/security/THREAT_MODEL.md` · `docs/security/DATA_CLASSIFICATION.md` ·
`docs/security/AUDIT_MODEL.md`.


> **Nota sulle citazioni dell'app `cases`.** I numeri di riga di `apps/cases/*` si riferiscono
> allo stato del **20 settembre 2026**: l'app è stata aggiunta a `INSTALLED_APPS`
> (`config/settings/base.py:67`) nella stessa giornata ed era in costruzione attiva. Le righe
> vanno riverificate alla prima revisione; i simboli citati (`readable_by`, `is_live`,
> `case_detail`, `record_assessment`, `reproduce`) sono il riferimento stabile.

---

## 1. I tre principi, e che cosa significano nel codice

### 1.1 Deny by default

Non «tutto è vietato tranne ciò che permettiamo» come slogan, ma come **comportamento predefinito
della funzione di autorizzazione**:

```python
# apps/accounts/permissions.py:36-45
def can(user, action: str, obj) -> bool:
    if user is None or not getattr(user, "is_authenticated", False) or not user.is_active:
        return False
    if roles.is_superadmin(user):
        return True
    for klass in type(obj).__mro__:
        func = _POLICIES.get(klass)
        if func is not None:
            return bool(func(user, action, obj))
    return False          # ← nessuna policy registrata = nessun accesso
```

Un modello senza policy è **inaccessibile**, non accessibile a tutti. Aggiungere un modello e
dimenticare la policy produce un 403, non una fuga di dati. Questo è il singolo pezzo di codice più
importante del modello autorizzativo. **IMPLEMENTATO.**

`require(user, action, obj)` solleva `PermissionDenied` `apps/accounts/permissions.py:48-50`.

### 1.2 Minimo privilegio

Un ruolo riceve **solo** i permessi del lavoro che deve fare. Oggi i permessi di modello per gruppo
sono dichiarati in un'unica tabella esplicita, e ciò che non è elencato non è concesso
`apps/accounts/roles.py:39-78`. Le implicazioni negative sono visibili: `role:staff` ha
`view/change/add` su nove app, comprese le richieste delle imprese
(`roles.py:44-56`) — vedi §7, lacuna L-03.

### 1.3 Separazione dei compiti

Chi esegue non approva; chi scrive una regola non la attiva; chi amministra i contenuti non
amministra le persone. Oggi:

| Separazione richiesta | Stato |
|---|---|
| L'autore di una regola non la approva (D2 §4, REQ-RUL-10) | **DESIGN ONLY** — nessun workflow di approvazione esiste |
| Il Legal/Rule Editor non ottiene privilegi di superadmin (REQ-IAM-10) | **DESIGN ONLY** — il ruolo non esiste |
| L'amministratore non può concedersi il superadmin | **IMPLEMENTATO** — lacuna L-01 (T-04) chiusa, vedi §7.1: `UserAdmin` nasconde e rifiuta `is_superuser` e i gruppi protetti; prova `tests/security/test_privilege_escalation.py::test_an_administrator_cannot_grant_superuser_to_themselves` (e gli altri test del file) |
| Il redattore di contenuti non accede ai fascicoli | **PARZIALE** — il ruolo non esiste come tale, il lavoro è su `role:staff` |
| La pubblicazione di un testo legale è tracciata | **IMPLEMENTATO** — `legal.published` / `legal.unpublished` `apps/legal/services.py:69-83` |

### 1.4 La regola che decide tutto il resto

> **Un identificativo scoperto a mano non aggira mai un controllo.**
> (direttiva di rebase §61, criterio di accettazione D2 §17)

Nessun oggetto è accessibile perché se ne conosce l'UUID, il riferimento o la posizione in una lista.
L'identificativo è un **indirizzo**, non una **credenziale**. Ogni percorso di lettura riparte dalla
domanda «questo utente può vedere questo oggetto?», anche quando l'oggetto è già in memoria, anche
quando è arrivato da un link interno, anche quando è il «proprio» oggetto secondo l'interfaccia.

---

## 2. I quindici ruoli

Ruoli di dominio da `PLATFORM_REQUIREMENTS_V2.md` §2, confrontati con i gruppi Django realmente
esistenti in `apps/accounts/roles.py`. Aggiornato il 21 settembre 2026: i sei ruoli mancanti sono
stati creati (**CR-10**, **REQ-IAM-04**).

| # | Ruolo di dominio | Gruppo | Stato | Vincolo invalicabile |
|---|---|---|---|---|
| 1 | **Persona** | `role:person` | **IMPL** (nessun permesso di modello) | Nessun accesso a dati di terzi |
| 2 | **Impresa** | `role:company` | **IMPL** (nessun permesso di modello) | Persone visibili solo con base giuridica, consenso e workflow autorizzato (**CR-04**) |
| 3 | **Soggetto autorizzato** | `role:authorised_actor` | **IMPL** | Assegnazione con estremo di autorizzazione e validità; scaduta non concede nulla |
| 4 | **Ente formativo** | `role:training_provider` | **IMPL** | Solo i dati necessari alla formazione; nessun fascicolo |
| 5 | **Professionista** | `role:professional` | **IMPL** | Solo i fascicoli espressamente assegnati; **MFA obbligatoria** |
| 6 | **Istituzione** | `role:institution` | **IMPL** | Perimetro definito da convenzione (modello `Agreement` ancora assente — L-11) |
| 7 | **Università** | `role:university` | **IMPL** | Nessun accesso ai fascicoli |
| 8 | **Moderazione** | `role:moderator` | **IMPL** — `community: view, change` | Community e contenuti segnalati |
| 9 | **Redattore di contenuti** | `role:content_editor` | **IMPL** | Contenuti editoriali; **nessun** accesso ai fascicoli né agli account |
| 10 | **Legal/Rule Editor** | `role:legal_editor` | **IMPL** — `rules: view, change, add` | Redige, **non approva**; nessun altro privilegio. Incompatibile con `legal_approver` |
| 10b | **Validazione giuridica** | `role:legal_approver` | **IMPL** — `rules: view, change` | Approva, **non crea**; non può approvare una regola di cui è autore |
| 11 | **Operatore** | `role:operator` | **IMPL** — `cases`, `helpdesk`, `enquiries` | Accede a un fascicolo solo tramite assegnazione; **MFA obbligatoria** |
| 12 | **Amministratore** | `role:administrator` | **IMPL** | Separazione dei privilegi, log obbligatori, MFA |
| — | *(fuori tassonomia)* | `role:staff` | **IMPL** | Lavorazione editoriale quotidiana. **Da ridurre** (L-03): `content_editor` e `operator` ne assumono le due metà |
| — | *(fuori tassonomia)* | `role:superadmin` | **IMPL** | Scavalca ogni policy: `can()` in `permissions.py`, `has_role()` in `roles.py` |

**Le due confusioni sono sciolte.** Università ed ente formativo hanno ora gruppi distinti, con
perimetri diversi: l'università non vede fascicoli, l'ente formativo vede i dati di formazione delle
persone assegnate e nulla di più. Redattore e operatore sono separati; resta da alleggerire
`role:staff`, che li precede entrambi (L-03).

**Incompatibilità dichiarata.** `role:legal_editor` e `role:legal_approver` non possono coesistere
sullo stesso account: `roles.INCOMPATIBLE_ROLES`, applicato in `assign_role` e nel form dei gruppi
dell'admin. È la condizione perché la revisione a quattro occhi significhi qualcosa.

**MFA per responsabilità, non per URL.** `services.MFA_REQUIRED_ROLES` la richiede a chiunque possa
leggere il fascicolo di un'altra persona — professionista, soggetto autorizzato, operatore, ruoli
giuridici, redazione e amministrazione — e non soltanto a chi ha `is_staff`. Un professionista
assegnato legge la situazione giuridica di una persona senza alcun flag di staff: legare la seconda
prova al flag significava proteggere la porta sbagliata (L-10).

**Attivare e presentare sono due regole (F-5).** `BACKOFFICE_MFA_ENFORCED` rende obbligatoria
l'attivazione del TOTP per questi ruoli; un account che ha già un dispositivo lo presenta in ogni
sessione prima del back-office, dell'area riservata e di `/documents/`, qualunque sia il valore del
flag (`accounts.services.second_factor_due`). L'attivazione prova che un dispositivo esiste, non che
la persona alla tastiera lo abbia: per questo il modulo di accesso proprio del back-office, che non
chiedeva il codice, non autentica più nessuno.

**«Candidato» non è un ruolo** (**CR-09**): è uno stato della persona dentro un processo di
selezione, rappresentato da `SelectionProcess.stage`. Non deve mai comparire fra i gruppi.

### 2.1 Permessi di modello concessi oggi

`ROLE_PERMISSIONS` `apps/accounts/roles.py:39-78`, applicati da `ensure_roles()` `:81-93`:

| Gruppo | App e azioni |
|---|---|
| `role:moderator` | `community`: view, change |
| `role:staff` | `enquiries`: view, change · `forum`, `news`, `faq`, `glossary`, `living`, `cms`, `partners`: view, change, add · `pathways`: view, change · `consents`, `notifications`: view · `community`: view, change |
| `role:administrator` | quanto sopra con `delete` dove previsto, più `orientation` (view, change, add), `accounts` (view, change), `audit` (view), `core` (view, change), `legal` (view, change), `documents` (view), `integrations` (view) |
| `role:person`, `role:company`, `role:institution`, `role:university`, `role:professional` | **nessuno** |
| `role:superadmin` | nessun permesso esplicito: scavalca le policy per codice |

Conseguenze da leggere con attenzione:

- i cinque ruoli «di piattaforma» non hanno **alcun** permesso di modello: tutto ciò che possono fare
  passa dalle policy a livello di oggetto e dalle viste dell'area riservata. È corretto ed è anche
  il motivo per cui oggi non esiste fuga di dati per ruolo: **non esiste ancora il workspace**;
- `role:administrator` riceve `accounts: change`, cioè `change_user`: è l'origine della lacuna L-01;
- nessun ruolo riceve permessi sull'app `auth`: i gruppi non si creano né si modificano dal
  back-office, ma si possono **assegnare** dal form utente.

---

## 3. Dove avviene il controllo

Tre livelli, nell'ordine in cui devono essere attraversati. **Il livello 1 non è facoltativo.**

```
  richiesta
      │
      ▼
 ┌──────────────────────────────────────────────────────────────────┐
 │ 1. QUERYSET — l'autorizzazione è parte della query               │
 │    Model.objects.readable_by(user) …                             │
 │    Ciò che l'utente non può vedere NON ESISTE per lui:           │
 │    non nelle liste, non nei conteggi, non negli autocomplete,    │
 │    non nei risultati di ricerca, non nelle aggregazioni.         │
 └──────────────────────────────────────────────────────────────────┘
      │
      ▼
 ┌──────────────────────────────────────────────────────────────────┐
 │ 2. OGGETTO — require(user, action, obj)                          │
 │    Seconda difesa su un oggetto già in mano. Deny by default.    │
 │    Verifica anche l'azione: "view" ≠ "change" ≠ "delete".        │
 └──────────────────────────────────────────────────────────────────┘
      │
      ▼
 ┌──────────────────────────────────────────────────────────────────┐
 │ 3. TEMPLATE — decide solo che cosa MOSTRARE                      │
 │    {% if can_edit %} nasconde un bottone.                        │
 │    NON È UN CONTROLLO DI SICUREZZA. Mai il solo livello.         │
 └──────────────────────────────────────────────────────────────────┘
```

### 3.1 Perché il livello 1 è obbligatorio

Filtrare dopo aver letto (`[o for o in qs if can(user, "view", o)]`) è sbagliato per quattro motivi:

1. i **conteggi** e la paginazione rivelano quante righe esistono;
2. gli **aggregati** (`Count`, `Sum`, medie) includono righe non autorizzate;
3. la **ricerca** restituisce «0 risultati» oppure «risultato oscurato»: due risposte diverse, quindi
   un oracolo di esistenza;
4. la **prestazione** degrada e spinge, prima o poi, a saltare il filtro.

Esempio corretto, già presente:

```python
# apps/cases/models.py:106-124
class CaseFileQuerySet(models.QuerySet):
    def readable_by(self, user) -> CaseFileQuerySet:
        """Authorisation applied AT QUERY TIME, never after the fact."""
```

e la sua lettura:

```python
# apps/cases/services.py:346-352
def case_detail(user, uuid_value) -> CaseFile:
    case = CaseFile.objects.readable_by(user).filter(uuid=uuid_value).first()
    if case is None:
        raise PermissionDenied   # indistinguibile da «non esiste»
    return case
```

Lo stesso schema è già in uso nel Forum Virtuale: `services.rooms_for`,
`services.visible_discussions`, `services.visible_posts` filtrano la query
(`apps/community/services.py:58-82`) e la vista aggiunge `require(...)` sull'oggetto
(`apps/community/views.py:130,169,211,234,261,277`). **È il modello da generalizzare.**

### 3.2 Ricerca

> «Un utente non deve **mai** scoprire l'esistenza di un oggetto non autorizzato attraverso i
> risultati. L'autorizzazione si applica **durante** la valutazione della query, non dopo.»
> (`PLATFORM_REQUIREMENTS_V2.md` §15)

Regole vincolanti per qualsiasi ricerca di piattaforma:

- si parte **sempre** da `readable_by(user)` e si aggiungono i criteri testuali, mai il contrario;
- nessun suggerimento, autocomplete o conteggio costruito su una queryset non filtrata;
- nessun indice a testo pieno che unisca righe di utenti diversi senza colonna di appartenenza;
- i risultati non mostrano frammenti di campi che il ruolo non potrebbe leggere nel dettaglio;
- la ricerca pubblica (guide, FAQ, glossario, attualità) opera solo su contenuto `PUB`: oggi è così
  (`apps/glossary/services.py:100-114`, `apps/faq/services.py`) e non deve mai essere estesa ai
  modelli di dominio.

### 3.3 Il livello 3 non protegge nulla

Nascondere un bottone non impedisce una richiesta POST. Ogni vista che espone un'azione deve
ripetere il controllo lato server. Verificato oggi: le viste del portale chiedono la proprietà anche
quando la policy sarebbe più permissiva `apps/portal/services.py:112-118,404-415` e le viste del
Forum chiamano `require` prima di ogni azione.

### 3.4 Chi scavalca, e perché è un rischio accettato ma tracciato

`superadmin` (e `is_superuser`) restituisce `True` prima di consultare qualunque policy
`apps/accounts/permissions.py:39-40`, e `has_role` è vera per ogni ruolo `apps/accounts/roles.py:110-111`.
È una scelta di progetto (serve un'ultima risorsa amministrativa), ma implica:

- il numero di superadmin è minimo, nominativo e rivisto periodicamente;
- l'accesso avviene solo da `/backoffice/` con MFA, presentata nella sessione (`apps/accounts/middleware.py`, `apps/accounts/admin_site.py`);
- **ogni** azione va tracciata: oggi lo sono le scritture via admin `apps/audit/signals.py:12-24`,
  **non** le letture (vedi `AUDIT_MODEL.md` §3.2).

### 3.5 Il back-office non concede più della piattaforma (F-8, ottobre 2026)

Un permesso di modello apre una schermata del back-office, e `ROLE_PERMISSIONS` lo concede per applicazione, mai per riga: fino a F-8 `role:operator` elencava e apriva in `/backoffice/` ogni fascicolo, ogni assegnazione e ogni pre-valutazione che sulla piattaforma non vede, e altri ruoli leggevano o modificavano lì ciò che la loro policy nega. Ora ogni schermata con dati personali chiede anche la regola della piattaforma (`core.admin_base.PolicyBoundAdminMixin`): le righe vengono dalla stessa queryset (`readable_by`), ogni oggetto passa dalla stessa policy (`can`), la schermata si apre ai soli ruoli che la policy nomina. L'operatore vede i fascicoli di cui ha un'assegnazione viva, nessuna richiesta dello sportello (le assegna sulla piattaforma), nessuna richiesta pubblica; la moderazione del Forum Virtuale è dei moderatori, il modulo di governance del Forum dell'amministratore, il revisore giuridico legge la sola traccia di audit delle regole, le risposte al questionario restano del titolare; il superuser resta l'ultima risorsa (§3.4). Ciò che scrive il dominio è in sola lettura (finalità e percorso del fascicolo, responsabile di una voce di checklist); lo stato di una voce passa da `cases.services.set_checklist_status`, con il suo evento di audit; un fascicolo `CLOSED` è in sola lettura per tutti, amministratore e superuser compresi — la sola eccezione voluta è la cancellazione, che chiude un fascicolo per conservazione e non lo modifica. Un permesso di sola lettura non scrive mai (reinvio, annullamento, revoca di un consenso e rimessa in coda richiedono `change` e sono tracciati), nessun token di un interessato è mostrato, e un privilegio di staff esercitato su un percorso pubblico — moderazione, anteprime di contenuti non pubblicati — chiede il secondo fattore come il back-office (`accounts.middleware.require_second_factor`). Prove: `apps/cases/tests/test_backoffice_follows_the_policy.py`, `tests/backoffice/test_screens_follow_the_policies.py`, `apps/accounts/tests/test_second_factor_wherever_the_privilege_lives.py`; dettaglio e domande aperte in `docs/design-v5/QA/v54/sec-f8/NOTES.md`.

Dopo la revisione indipendente (F8R-1…F8R-3): le azioni del flusso delle regole giuridiche chiedono `rules.policies` come ogni altro ingresso — approvare, mettere in vigore e ritirare sono del `role:legal_approver` (mai dell'autore), mai di un permesso di sola lettura né del redattore, e il revisore legge il testo che approva senza poterlo riscrivere; un campo che una schermata nasconde non è nemmeno un filtro né una ricerca della lista (`core.admin_base.BaseModelAdmin.hidden_fields`: i token di un iscritto, il corpo di un'e-mail per chi ha la sola lettura, le risposte al questionario); a chi non può aprire gli account nessun modulo e nessun filtro elenca un account — i campi che puntano a un account sono in sola lettura e li valorizza il flusso (l'autore alla creazione, il revisore con l'azione di revisione). Prove: `apps/rules/tests/test_backoffice_follows_the_policy.py`, `tests/backoffice/test_a_hidden_field_is_no_filter.py`, `tests/backoffice/test_forms_name_no_account.py`.

---

## 4. Regole a livello di oggetto

Vocabolario usato nelle matrici del §5:

| Cella | Significato |
|---|---|
| `none` | Nessun accesso. Il tentativo restituisce 404 (preferito) o 403 |
| `own` | Solo le righe di cui l'utente è titolare (`person`, `owner`, `recipient`, `author`) |
| `assigned` | Solo le righe per cui esiste un'assegnazione **viva** (non revocata **e** non scaduta) |
| `scope` | Solo entro un perimetro dichiarato da un oggetto di accordo/convenzione o da una relazione (organizzazione, fabbisogno, coorte) |
| `all` | Tutte le righe del modello |
| `(D)` | **DESIGN ONLY**: la regola è decisa, l'oggetto o il codice non esistono |

### 4.1 Le sette regole di dominio

| # | Regola | Fonte | Stato oggi |
|---|---|---|---|
| R-1 | **La persona possiede il proprio fascicolo**: lo vede sempre, lo modifica solo finché è attivo, non può modificarne lo stato né gli elementi la cui responsabilità è di un altro attore | D2 §8-9 | `apps/cases/policies.py:49-68,71-…` — **PARZ** (nessuna vista) |
| R-2 | **L'impresa possiede i propri fabbisogni**, non le persone. Nessun elenco di persone, nessuna scheda candidato per difetto | D2 §17, RB §29, **CR-04** | `(D)` per `CompanyNeed`; oggi vero per assenza del modulo |
| R-3 | **Il soggetto autorizzato vede solo i processi di selezione assegnati**, con autorizzazione valida e non scaduta; la catena `CompanyNeed → AuthorizedActor → SelectionProcess → CaseFile → AuditEvent` non ammette scorciatoie | D2 §9, **CR-03** | `(D)` |
| R-4 | **Il professionista vede solo i fascicoli espressamente assegnati**, con mandato dove necessario | D2 §4, RB §38 | `apps/cases/policies.py` prevede `AssignmentRole.PROFESSIONAL` — **PARZ** |
| R-5 | **L'ente formativo vede solo i dati della formazione assegnata**: non il fascicolo, non i documenti, non l'esito dell'orientamento | D2 §4, RB §37 | `(D)` — il ruolo non esiste nemmeno |
| R-6 | **L'istituzione vede solo ciò che l'accordo prevede**: progetti, indicatori aggregati, documenti condivisi. Mai fascicoli individuali | D2 §4 | `(D)` — manca il modello `Agreement` |
| R-7 | **L'università non accede ad alcun fascicolo privato**: il divieto è strutturale, non una vista mancante | D2 §4, REQ-UNI-02 | `(D)` — da garantire con l'assenza di relazione, non solo di interfaccia |

### 4.2 Assegnazione: cosa rende un'assegnazione «viva»

Una `CaseAssignment` autorizza **solo** se, nel momento della verifica:

1. `revoked_at IS NULL`;
2. l'autorizzazione non è scaduta (`authorisation_valid_until` assente o futura);
3. il caso non è chiuso in modo che escluda quel ruolo;
4. l'account dell'assegnatario è attivo.

Il modello prevede i campi `revoked_at` e `authorisation_valid_until` `apps/cases/models.py:333,336`
e la proprietà `is_live` `apps/cases/models.py:347-351`, che la policy usa `apps/cases/policies.py:42-46`. **La queryset no**: filtra solo `revoked_at__isnull=True`
`apps/cases/models.py:121`. Finché i due non coincidono, una lista può mostrare ciò che un dettaglio
nega — e un mandato scaduto continua a produrre righe (T-09). **Un solo predicato, usato da
entrambi.**

### 4.3 Il consenso è una condizione di accesso, non un ricordo

Per i casi previsti da **CR-04** (visibilità della persona da parte dell'impresa), l'esistenza di un
`ConsentRecord` attivo per la finalità va verificata **al momento della lettura**, non solo alla
creazione del processo: un consenso revocato deve chiudere l'accesso immediatamente.
`ConsentRecord.is_active` esiste `apps/consents/models.py:78`; il collegamento alla policy è
**DESIGN ONLY**.

---

## 5. Matrice dei permessi

Legenda in §4. `R` = lettura, `W` = creazione/modifica, `D` = cancellazione.
La colonna **Stato** dice se la riga è applicata dal codice.

### 5.1 `CaseFile` — fascicolo digitale

| Ruolo | R | W | D | Note |
|---|---|---|---|---|
| Persona | own | own | none | Modifica solo finché il caso è attivo (`is_read_only`) |
| Impresa | none | none | none | Mai: l'impresa vede fabbisogni, non fascicoli |
| Soggetto autorizzato | assigned `(D)` | none `(D)` | none | Agisce sul `SelectionProcess`, non sul fascicolo |
| Ente formativo | none `(D)` | none | none | Vede `Enrollment`, non il fascicolo |
| Professionista | assigned | assigned | none | Solo assegnazioni vive |
| Istituzione | none | none | none | Solo aggregati, fuori da questo modello |
| Università | none | none | none | Divieto strutturale (R-7) |
| Moderazione | none | none | none | — |
| Redattore di contenuti | none | none | none | — |
| Legal/Rule Editor | none | none | none | Lavora su regole, non su persone |
| Operatore | assigned `(D)` | assigned `(D)` | none | Perimetro ristretto |
| Amministratore | all | all | all | Tracciato |

**Stato**: queryset `readable_by` **IMPLEMENTATA** `apps/cases/models.py:106-124`; policy per oggetto
**IMPLEMENTATA** `apps/cases/policies.py:49-68`; **nessuna vista, nessun template, nessun test di
permesso end-to-end** → il perimetro non è ancora esercitato. Il ramo `role:staff` della queryset
restituisce oggi tutte le righe (`Q(pk__isnull=False)` `:123`): **da sostituire con un perimetro
esplicito**.

### 5.2 `ChecklistItem`

| Ruolo | R | W | D | Note |
|---|---|---|---|---|
| Persona | own (via caso) | own **solo** gli elementi con `responsible_actor = PERSON` | none | Non può attestare l'azione di un'autorità |
| Impresa | none | none | none | — |
| Soggetto autorizzato | assigned `(D)` | assigned, solo i propri elementi `(D)` | none | — |
| Ente formativo | none `(D)` | none | none | — |
| Professionista | assigned | assigned | none | — |
| Istituzione / Università | none | none | none | — |
| Moderazione / Redattore / Legal Editor | none | none | none | — |
| Operatore | assigned `(D)` | assigned `(D)` | none | — |
| Amministratore | all | all | all | — |

**Stato**: policy **IMPLEMENTATA** con la restrizione per `responsible_actor`
`apps/cases/policies.py:71-80`; nessuna vista.

### 5.3 `Document` (`documents.PrivateDocument`)

| Ruolo | R (download) | W (upload/sostituzione) | D | Note |
|---|---|---|---|---|
| Persona | own | own | own (soft delete) | Il proprietario può scaricare anche i file `pending` |
| Impresa | own + scope (responsabile dell'organizzazione) | own | own | `MembershipRole.OWNER` dell'organizzazione indicata |
| Soggetto autorizzato | assigned `(D)` | none `(D)` | none | Solo i documenti del processo assegnato |
| Ente formativo | none `(D)` | none | none | — |
| Professionista | assigned `(D)` | none `(D)` | none | Oggi **non** previsto dalla policy |
| Istituzione / Università | none | none | none | — |
| Moderazione | none | none | none | Esplicitamente escluso dai test `test_download.py:84` |
| Redattore / Legal Editor | none | none | none | — |
| Operatore | assigned `(D)` | none | none | — |
| Amministratore | all (solo `clean`) | none | none | `role:staff` e `role:administrator` scaricano solo i file analizzati |

**Stato**: **IMPLEMENTATA** e testata `apps/documents/policies.py:26-38`,
`apps/documents/views.py:97-115`, `apps/documents/tests/test_download.py`. Le righe `assigned` sono
**DESIGN ONLY**: la policy non conosce ancora fascicoli e assegnazioni.

### 5.4 `CompanyNeed` *(oggi: `enquiries.CompanyNeedsRequest`, un form pubblico)*

| Ruolo | R | W | D | Note |
|---|---|---|---|---|
| Persona | none | none | none | — |
| Impresa | own | own `(D)` | none | Oggi: solo lettura della propria richiesta inviata |
| Soggetto autorizzato | assigned `(D)` | none | none | Vede il fabbisogno su cui è incaricato |
| Ente formativo | scope `(D)` | none | none | Solo il fabbisogno formativo collegato al piano |
| Professionista | none | none | none | — |
| Istituzione | aggregati `(D)` | none | none | Mai la singola impresa con i dati di contatto |
| Università | none | none | none | — |
| Moderazione / Redattore / Legal Editor | none | none | none | — |
| Operatore | scope `(D)` | scope `(D)` | none | Lavorazione assegnata |
| Amministratore | all | all | all | — |

**Stato**: `enquiries.PublicSubmission` ha una policy **IMPLEMENTATA** (proprietario + back-office)
`apps/enquiries/policies.py:18-21`. Il `CompanyNeed` gestibile di D2 §9 è **DESIGN ONLY**
(REQ-B2B-02/04).

### 5.5 `SelectionProcess`

| Ruolo | R | W | D | Note |
|---|---|---|---|---|
| Persona | own (il proprio stato nel processo) | none | none | Deve sapere di essere in una selezione |
| Impresa | scope, **campi ridotti**, solo con consenso attivo | none | none | **CR-04**: in P0 la visibilità è **zero** |
| Soggetto autorizzato | assigned | assigned | none | È il responsabile: sempre identificato (D2 §17.6) |
| Ente formativo | none | none | none | — |
| Professionista | assigned (se collegato al fascicolo) | none | none | — |
| Istituzione / Università | none | none | none | — |
| Moderazione / Redattore / Legal Editor | none | none | none | — |
| Operatore | assigned | assigned | none | — |
| Amministratore | all | all | none | Nessuna cancellazione: è materia di audit |

**Stato**: **DESIGN ONLY** in tutte le celle. Vincoli non negoziabili alla costruzione: nessuna
creazione senza `AuthorizedActor` valido; ogni transizione genera `AuditEvent`; nessuna vista
pubblica; nessun elenco di persone (CR-03).

### 5.6 `LegalRule` *(oggi: `orientation.Rule` dentro un `Ruleset`)*

| Ruolo | R | W | D | Note |
|---|---|---|---|---|
| Persona … Università | none (la **condizione**) | none | none | L'esito e le fonti sono pubblici; la logica no |
| Moderazione | none | none | none | — |
| Redattore di contenuti | none | none | none | Può tradurre i testi, non toccare le condizioni |
| **Legal/Rule Editor** | all | all in `DRAFT`; propone il passaggio a `LEGAL_REVIEW` | none | **Non approva ciò che ha scritto** |
| Revisore legale *(secondo paio d'occhi)* | all | approva / respinge | none | Persona diversa dall'autore |
| Operatore | none | none | none | — |
| Amministratore | all | attiva un ruleset approvato | none | Non entra nel merito giuridico |

**Stato**: `role:administrator` ha oggi `orientation: view, change, add` `apps/accounts/roles.py:65`;
non esistono `LEGAL_RULE_EDITOR`, `review_status`, `approved_by`, `approved_at`, né il workflow a
quattro occhi. **Una regola non si cancella mai**: si ritira (`RETIRED`), perché gli esiti passati
devono restare riproducibili. **DESIGN ONLY** (REQ-RUL-02, REQ-RUL-10, REQ-RUL-12).

### 5.7 `Enrollment` *(Academy)*

| Ruolo | R | W | D | Note |
|---|---|---|---|---|
| Persona | own | own (iscrizione) | own (ritiro) | Accesso **indipendente** da qualsiasi selezione (**CR-14**) |
| Impresa | none | none | none | Nessun accesso ai progressi individuali |
| Soggetto autorizzato | assigned, solo stato di completamento | none | none | — |
| **Ente formativo** | assigned (coorte/corso assegnato) | assigned (valutazioni, completamento) | none | **Solo i dati necessari alla formazione** (R-5) |
| Professionista | assigned, se utile al fascicolo | none | none | — |
| Istituzione | aggregati | none | none | Numeri, non nomi |
| Università | scope (propri programmi) | scope | none | — |
| Moderazione / Redattore / Legal Editor | none | none | none | — |
| Operatore | assigned | assigned | none | — |
| Amministratore | all | all | none | — |

**Stato**: **DESIGN ONLY** (REQ-EDU-01…07).

### 5.8 `ForumProposal` *(Forum come modulo di governance)*

| Ruolo | R | W | D | Note |
|---|---|---|---|---|
| Persona | none, salvo partecipante | none | none | La partecipazione è un'appartenenza, non il ruolo |
| Impresa / Istituzione / Università / Ente formativo | scope (commissioni e tavoli di appartenenza) | own (proprie proposte) | own in bozza | — |
| Soggetto autorizzato / Professionista | scope, se partecipanti | own | own in bozza | — |
| Moderazione | all nei tavoli moderati | change (stato di moderazione) | none | — |
| Redattore di contenuti | pubblicazione degli esiti | none | none | — |
| Legal/Rule Editor | none | none | none | — |
| Operatore | scope | scope | none | — |
| Amministratore | all | all | all | — |

**Regola invalicabile**: «i partecipanti del Forum non possono consultare informazioni private di
altri utenti» (RB §61, REQ-FOR-06). Il modello attuale del Forum Virtuale la rispetta con l'opt-in
`show_name` / `show_organisation`, entrambi `False` per difetto `apps/community/models.py:71-74`.

**Stato**: `community` **IMPLEMENTATO** (dietro flag `virtual_forum`, chiuso) con policy per stanza,
discussione, post, segnalazione `apps/community/policies.py:56-140`. `ForumProposal`,
`Commission`, `Table`, `Project`, `Milestone`: **DESIGN ONLY** (REQ-FOR-02/03/04).

### 5.9 `AuditEvent`

| Ruolo | R | W | D |
|---|---|---|---|
| Persona | own `(D)` — «cronologia delle attività» nel proprio fascicolo | none | none |
| Impresa … Operatore | none | none | none |
| **Amministratore** | all (sola lettura) | none | none |
| **Superadmin** | all (sola lettura) | none | none |
| *Revisore esterno / DPO* | all (sola lettura, accesso nominativo) `(D)` | none | none |
| **Sistema** | — | **insert** | none |

**Nessun ruolo ha `W` o `D`.** L'unico scrittore è il sistema, in append.
**Stato**: **IMPLEMENTATO nell'interfaccia** `apps/audit/admin.py:13-22` + `audit: view` per
l'amministratore `apps/accounts/roles.py:72`; **non a livello di storage** (vedi `AUDIT_MODEL.md` §4).

### 5.10 `User`

| Ruolo | R | W | D | Note |
|---|---|---|---|---|
| Persona … Operatore | own | own (campi di profilo in allowlist) | own (cancellazione = anonimizzazione) | Nessun id utente nelle URL `apps/accounts/views.py:1-3` |
| Moderazione | scope (partecipanti della community) | none | none | Solo ciò che la moderazione richiede |
| **Amministratore** | all | all **tranne** `is_superuser`, `is_staff`, `groups` | none | La cancellazione è anonimizzazione, non `DELETE` |
| **Superadmin** | all | all, compresi i privilegi | none | Ogni concessione di privilegio è un evento di audit dedicato |

**Stato**: **PARZIALE.** La concessione del superadmin è chiusa (lacuna L-01, T-04, §7.1):
`UserAdmin` nasconde e rifiuta `is_superuser`, toglie `role:superadmin` e `role:administrator` dalle
scelte di `groups` e rende intoccabili gli account superuser (`apps/accounts/admin.py`, prova
`tests/security/test_privilege_escalation.py`). Resta più largo della riga «tranne»: l'amministratore
imposta ancora `is_staff` e i gruppi ordinari — è così che si creano gli account del personale —, una
differenza documentata e lasciata alla decisione del titolare (domanda Q-1,
`docs/design-v5/QA/v54/sec-f8/NOTES.md` §6).

### 5.11 `Consent`

| Ruolo | R | W | D | Note |
|---|---|---|---|---|
| Persona … Operatore | own | own (concessione e revoca) | **none** | La prova non si cancella: si revoca |
| Redattore di contenuti | none | none | none | I testi bloccati non sono modificabili |
| Amministratore | all | registrazione della revoca; nuova **versione** del testo | none | Nessuna modifica retroattiva di un testo già mostrato |
| Superadmin | all | idem | none | — |

**Stato**: **IMPLEMENTATO**. `ConsentText` versionato con `locked_key` per i testi prescritti
(read-only nell'admin); `ConsentRecord` punta alla versione mostrata; `withdraw` non cancella
(`apps/consents/`, `docs/PRIVACY_BY_DESIGN.md` §3). `role:staff` ha `consents: view`,
`role:administrator` `view, change, add` — **mai `delete`** `apps/accounts/roles.py:53,68`.

### 5.12 Riepilogo dello stato di applicazione

| Oggetto | Queryset | Policy oggetto | Viste | Test | Verdetto |
|---|---|---|---|---|---|
| `PrivateDocument` | `for_owner` `apps/documents/models.py:40-41` | sì `policies.py:26-38` | sì | sì `tests/test_download.py` | **IMPLEMENTATO** |
| `Message`, `Deadline`, `PortalNotice` | `inbox()`, filtro per proprietario | sì `apps/portal/policies.py:48-78` | sì | sì `apps/portal/tests/test_security.py` | **IMPLEMENTATO** |
| `OrientationSession`, `OrientationResult` | accesso per sessione/token/utente | sì `apps/orientation/policies.py:9-18` | sì | sì | **IMPLEMENTATO** |
| `PublicSubmission` | filtro per proprietario | sì `apps/enquiries/policies.py:18-21` | sì | sì | **IMPLEMENTATO** |
| `ForumRegistration` | — | sì `apps/forum/permissions.py:10-21` | back-office | sì | **IMPLEMENTATO** |
| Community (`Room`…`Initiative`) | `rooms_for`, `visible_*` `apps/community/services.py:58-82` | sì `apps/community/policies.py:56-140` | sì | sì `test_permissions.py` | **IMPLEMENTATO** (dietro flag) |
| `CaseFile`, `ChecklistItem`, `CaseAssignment`, `PathwayAssessment` | `readable_by` `apps/cases/models.py:106-124` | sì `apps/cases/policies.py` | **no** | parziale | **PARZIALE** |
| `CompanyNeed`, `SelectionProcess`, `AuthorizedActor`, `Enrollment`, `TrainingPlan`, `LegalRule`, `ForumProposal`, `Agreement` | — | — | — | — | **DESIGN ONLY** |

---

## 6. Regole per chi scrive codice

Checklist vincolante per ogni modello di dominio nuovo. Una riga non spuntata = la PR non passa.

1. **Policy registrata** `@policy(Model)` prima ancora della prima vista. Senza, `can()` nega — ma
   una vista che non chiama `can()` non è protetta da nulla.
2. **Queryset di autorizzazione** `readable_by(user)` (o equivalente) sul manager del modello. Ogni
   lista, conteggio, aggregato e ricerca parte da lì.
3. **Azioni distinte**: `view`, `change`, `delete`, più le azioni di dominio (`download`,
   `mark_read`, `moderate`, `approve`). Mai un'unica azione «accesso».
4. **404, non 403**, per ciò che il chiamante non può vedere; 403 solo quando l'esistenza dell'oggetto
   è già legittimamente nota al chiamante.
5. **Nessun campo di autorità in un form**: `status`, `responsible_actor`, `assignee`, `approved_by`,
   `ruleset_snapshot`, `is_staff`, `is_superuser`, `groups` si cambiano solo da servizi di dominio o
   da un ruolo dedicato.
6. **Transizioni tramite servizio**, mai tramite `save()` da una vista: il servizio valida la
   transizione e registra l'`AuditEvent`.
7. **Test obbligatori** (marker `security`), come da RB §61 e D2 §17:
   - persona A non accede alla persona B;
   - impresa A non accede all'impresa B;
   - l'impresa non vede persone arbitrarie;
   - il professionista vede solo i casi assegnati;
   - l'ente formativo solo i dati di formazione autorizzati;
   - l'istituzione solo il perimetro di convenzione;
   - l'università nessun fascicolo privato;
   - i partecipanti del Forum nessuna informazione privata altrui;
   - il personale senza permesso non modifica le regole;
   - il Legal/Rule Editor non ottiene privilegi estranei;
   - **un identificativo scoperto a mano non aggira mai i permessi**;
   - un'assegnazione **revocata o scaduta** non dà più accesso;
   - la lista e il dettaglio danno la stessa risposta (nessuna riga visibile in lista e negata nel
     dettaglio, né viceversa).
8. **Audit**: ogni accesso a un fascicolo, ogni download, ogni cambio di assegnazione, ogni
   transizione sensibile (vedi `AUDIT_MODEL.md` §2).
9. **Riga nella matrice** del §5 di questo documento, aggiornata nella stessa PR.

---

## 7. Lacune note

Aggiornato il 21 settembre 2026, dopo il lavoro su rule engine, ruoli e permessi a livello di oggetto.

### 7.1 Chiuse

| ID | Lacuna | Come è stata chiusa | Prova |
|---|---|---|---|
| **L-01** | `role:administrator` poteva concedersi `is_superuser` o il gruppo `role:superadmin` | `UserAdmin` nasconde **e** rifiuta i campi di privilegio; i gruppi protetti sono ripristinati dopo il salvataggio della m2m | `tests/security/test_privilege_escalation.py` (13 test) |
| **L-02** | Il ruolo era auto-dichiarato alla registrazione | `register_declared_account_type`: solo `role:person` è concesso su dichiarazione; ogni altro tipo apre una verifica e non concede nulla | `apps/accounts/tests/test_account_verification.py` (15 test) |
| **L-04** | Sei ruoli su quindici non esistevano | Aggiunti `authorised_actor`, `training_provider`, `legal_editor`, `legal_approver`, `content_editor`, `operator`, con permessi minimi | `apps/accounts/tests/test_identity_gaps.py` |
| **L-05** | `readable_by` non applicava la scadenza dell'autorizzazione; `role:staff` riceveva tutte le righe | Predicato `is_live` nella queryset; `role:staff` non riceve nulla | `tests/security/test_object_permissions.py` §12, §13b |
| **L-06** | Fetch-then-check nel portale: la riga veniva caricata e poi rifiutata con 403 | L'autorizzazione è **nella query**: `Message.objects.inbox(user)`, `filter(pk=…, owner=user)` | `apps/portal/tests/test_security.py` |
| **L-07** | Risposte non uniformi: 403 sui documenti altrui, 404 sulle sessioni | Tutto ciò che il chiamante non può vedere risponde **404**, identico a ciò che non esiste | `test_security.py`, `test_object_permissions.py` §11 |
| **L-08** | Nessuna revoca di sessione alla revoca di un ruolo | `roles.revoke_role` chiama `services.revoke_sessions`: le sessioni aperte terminano subito | `test_identity_gaps.py::TestSessionRevocation` |
| **L-09** | Nessun instradamento post-login per ruolo | `AccountAdapter.get_login_redirect_url` porta ciascun ruolo alla propria superficie | `test_identity_gaps.py::TestPostLoginRouting` |
| **L-10** | MFA obbligatoria solo per `/backoffice/` | `MFA_REQUIRED_ROLES`: la richiede chiunque legga dati di terzi, anche senza `is_staff` — **e il middleware sorveglia ora anche l'area riservata**, non solo il back-office. Da F-5, un dispositivo già attivato va presentato in ogni sessione, qualunque sia `BACKOFFICE_MFA_ENFORCED` | `test_identity_gaps.py::TestSecondFactor`, `::TestTheSecondFactorIsEnforcedWhereItIsRequired`, `test_backoffice_second_factor.py` |
| **L-13** *(nuova)* | La policy di `CaseFile` concedeva a `role:staff` una vista che la queryset negava | Le due ora coincidono: solo proprietario, assegnatario vivo e amministratore | `test_object_permissions.py::test_13_the_list_and_the_object_check_agree` |
| **L-14** *(nuova)* | Nessun ruolo poteva più cancellare una comunicazione notificata: l'admin di Django rifiuta una cancellazione la cui cascata tocca un modello su cui l'account non ha `delete`, e `notifications.Notification` è legata a `portal.Message` in `CASCADE` | `ROLE_PERMISSIONS` accetta chiavi `app.model`: la concessione si ferma alla notifica e **non** raggiunge `EmailOutbox`. La cancellazione diretta di una notifica è ora tracciata | `apps/portal/tests/test_admin_cascade.py` (5 test) |

**L-10 era stata chiusa a metà.** La politica era stata allargata, l'applicazione no: il middleware
sorvegliava `/backoffice/`, dove un professionista non entra mai. `needs_backoffice_mfa` rispondeva
«sì, questo account deve iscriversi» e nessuno glielo chiedeva. Trovata da `manage.py check
--deploy`, il cui testo d'avviso descriveva ancora la regola stretta. **Una politica senza punto di
applicazione è un commento.**

**L-13 non era nota**: è stata trovata dall'asserzione §61 numero 13, che confronta la lista e il
controllo sull'oggetto per ogni ruolo. La metà permissiva è sempre il difetto, e qui era la policy.

**L-14 non è una regola scritta male: è una regola scritta altrove.** Il permesso su
`portal.Message` diceva di sì, il modello dei permessi diceva di sì, e l'accesso era comunque
negato — da una relazione dichiarata in un'altra applicazione. Il segnale era un 403 nudo, senza
pulsante mancante e senza testo. È il motivo per cui la concessione è per modello: la correzione
ovvia, `"notifications": ("delete",)`, avrebbe dato a un amministratore il potere di cancellare la
prova di ciò che è stato inviato.

### 7.2 Aperte

| ID | Lacuna | Gravità | Dove | Requisito |
|---|---|---|---|---|
| **L-03** | `role:staff` cumula redazione editoriale e accesso ai dati delle imprese | Media | `apps/accounts/roles.py` | REQ-IAM-05 |
| **L-11** | Nessun modello di convenzione (`Agreement`): il perimetro istituzionale non è verificabile dal codice | Media | assente | REQ-INS-01 |
| **L-12** | Nessuna verifica del consenso al momento della lettura per la visibilità impresa → persona | Alta quando arriverà la Fase P1 | assente | CR-04 |

`role:content_editor` esiste ora e può assumere la parte editoriale di `role:staff`: L-03 si chiude
spostando i permessi, non aggiungendo codice. Non è stato fatto in questa sede perché ridurre
`role:staff` mentre altre parti della piattaforma vi si appoggiano richiede di verificare ogni
chiamante, e la verifica vale più della fretta.

### 7.3 Separazione dei compiti

`role:legal_editor` e `role:legal_approver` sono dichiarati **incompatibili** in
`roles.INCOMPATIBLE_ROLES`. Il rifiuto è applicato in `assign_role` **e** nel form dei gruppi
dell'admin, perché un vincolo che un solo punto d'ingresso applica non è un vincolo. Un solo account
che redige e approva non è una revisione a quattro occhi: è lo stesso giudizio registrato due volte.

---

Classificazione di questo documento: **interno**
(`docs/source-of-truth/CONFIDENTIALITY_REGISTER.md` §2: mai esposto da una vista pubblica né in
documentazione API pubblica).
