# DOCUMENT SECURITY — ciclo di vita di un documento privato

Versione 1.0 · 20 settembre 2026 · Requisiti: **REQ-DOC-01…06**, **REQ-SEC-01**
Owner: referente tecnico · Revisione: a ogni nuovo tipo di documento, a ogni nuovo consumatore

Documenti correlati: `docs/security/THREAT_MODEL.md` (T-02, T-10, T-11) ·
`docs/security/DATA_CLASSIFICATION.md` (P-12, P-13) · `docs/security/PERMISSION_MODEL.md` §5.3 ·
`docs/security/AUDIT_MODEL.md`.


> **Nota sulle citazioni dell'app `cases`.** I numeri di riga di `apps/cases/*` si riferiscono
> allo stato del **20 settembre 2026**: l'app è stata aggiunta a `INSTALLED_APPS`
> (`config/settings/base.py:67`) nella stessa giornata ed era in costruzione attiva. Le righe
> vanno riverificate alla prima revisione; i simboli citati (`readable_by`, `is_live`,
> `case_detail`, `record_assessment`, `reproduce`) sono il riferimento stabile.

---

## 0. Il principio

Un documento caricato su questa piattaforma è, molto spesso, **una copia di un documento d'identità
di una persona che sta cercando di entrare regolarmente in un paese straniero**. Il danno di una
fuga non è «un file perso»: è furto d'identità, ricatto, esposizione della persona presso l'autorità
o il datore di lavoro. Da qui tre regole che non si negoziano:

1. **Il file non è mai raggiungibile per URL.** Nessuna chiave indovinabile, nessun percorso
   pubblico, nessun `MEDIA_URL`.
2. **Ogni consegna è un'autorizzazione**, ricalcolata al momento, mai ereditata da un link.
3. **Ogni consegna lascia una traccia.**

Marcatura: **IMPLEMENTATO** (verificato nel codice, citato) · **PARZIALE** · **RICHIESTO**
(decisione presa, codice assente) · **DESIGN ONLY**.

---

## 1. Panoramica del ciclo di vita

```
  UPLOAD ──► VALIDAZIONE ──► STORAGE ──► ANALISI AV ──► STATO
    │             │             │            │           │
    │             │             │            │           ├─► ACCESSO (lista, dettaglio)
    │             │             │            │           ├─► DOWNLOAD (autorizzato + audit)
    │             │             │            │           ├─► VERSIONI / SOSTITUZIONE   [RICHIESTO]
    │             │             │            │           ├─► SCADENZA                  [RICHIESTO]
    │             │             │            │           └─► CANCELLAZIONE ──► PURGA
    │             │             │            │
 rifiuto      rifiuto      nome casuale   pending/clean/
 (throttle)   (allowlist,  fuori dal      infected/error
              magic bytes) web root
```

Punti di ingresso oggi: **uno solo**, `POST /documents/upload/` `apps/documents/urls.py`.
Punti di uscita: **uno solo**, `GET /documents/<uuid>/` `apps/documents/views.py:97`.
Non esiste nessun'altra via per far entrare o uscire un file privato. È la proprietà più importante
del progetto di questa app e va difesa a ogni estensione.

---

## 2. Upload

| Controllo | Stato | Dove |
|---|---|---|
| Solo utenti autenticati | **IMPLEMENTATO** | `@login_required` `apps/documents/views.py:56` |
| Solo utenti che hanno accettato le Condizioni | **IMPLEMENTATO** | `services.user_may_upload` `apps/documents/services.py:241-243`; rifiuto con 403 e pagina dedicata `views.py:60-66` |
| Account attivo | **IMPLEMENTATO** | `user_may_upload` verifica `is_active` |
| Limite di frequenza | **IMPLEMENTATO** | 30 upload/ora per IP hashato `views.py:26,68-69` → pagina 429 |
| CSRF | **IMPLEMENTATO** | `CsrfViewMiddleware` `config/settings/base.py:90`; il form è POST con token |
| Nessuna cache della pagina | **IMPLEMENTATO** | `@never_cache` `views.py:57` |
| Limite di corpo della richiesta | **PARZIALE** | `DATA_UPLOAD_MAX_MEMORY_SIZE` / `FILE_UPLOAD_MAX_MEMORY_SIZE` = 5 MB `base.py:234-235` regolano la **memoria**, non la dimensione totale: il limite reale è quello applicativo (§3) e, in produzione, quello del reverse proxy (**da configurare**) |
| L'organizzazione indicata dev'essere una propria | **IMPLEMENTATO** | queryset ristretto alle appartenenze `apps/documents/forms.py:39`; test `tests/test_upload.py:244` |
| Descrizione limitata e normalizzata | **IMPLEMENTATO** | 200 caratteri `forms.py:21-26`, troncata anche nel servizio `services.py:264` |
| Avviso «non inserire dati sensibili» | **IMPLEMENTATO** nel form | `forms.py:25` — da estendere a tutti i campi liberi (`DATA_CLASSIFICATION.md` §5.3) |
| Quota per utente / per fascicolo | **RICHIESTO** | assente: un account può riempire il disco entro il limite di frequenza |

---

## 3. Validazione

La catena è unica e vive in `documents.services.validate_upload`
`apps/documents/services.py:158-183`. **Nessun percorso di caricamento può saltarla**: il form la
chiama in `clean_file` `apps/documents/forms.py:42-44` e il servizio la ripete in `store_upload`
`services.py:247`.

### 3.1 Allowlist di estensioni e MIME

**IMPLEMENTATO** — `apps/documents/services.py:44-49`:

| Estensione | MIME atteso |
|---|---|
| `.pdf` | `application/pdf` |
| `.jpg`, `.jpeg` | `image/jpeg` |
| `.png` | `image/png` |

Allowlist, non blocklist: ciò che non è elencato è rifiutato, senza eccezioni e senza
configurabilità a runtime. L'estensione è normalizzata in minuscolo prima del confronto
`services.py:106-108` (test `tests/test_upload.py:43`).

### 3.2 Perché SVG e HTML sono rifiutati

Non è una dimenticanza, è la ragione principale dell'allowlist.

| Formato | Perché è pericoloso |
|---|---|
| **SVG** | È XML, non un'immagine: può contenere `<script>`, `<foreignObject>`, `onload`, riferimenti esterni ed entità XML (XXE). Servito dalla stessa origine, esegue JavaScript nel contesto della piattaforma: furto di sessione, azioni a nome dell'utente. Nessuna sanificazione di SVG è affidabile a lungo termine |
| **HTML/HTM, XHTML** | Stessa ragione, senza nemmeno il travestimento |
| **Office (doc, docx, xls, xlsm)** | Macro, OLE, relazioni esterne: eseguono sul computer di chi apre, non sul server. Il danno colpisce l'operatore che riceve il documento |
| **Eseguibili e archivi (exe, msi, sh, zip, rar)** | Nessuna ragione funzionale; gli archivi nascondono qualunque cosa e aprono la via alle bombe di decompressione |
| **PDF con contenuto attivo** | Il PDF è ammesso perché indispensabile, ma **non** se contiene `/JavaScript`, `/JS` o `/Launch` (§3.4) |

La difesa non è solo l'allowlist: è l'allowlist **più** il fatto che nulla è mai servito in modo
renderizzabile (§7), **più** la CSP `object-src 'none'` `config/settings/base.py:330`.

### 3.3 Magic bytes: il contenuto deve corrispondere all'estensione

**IMPLEMENTATO** — `apps/documents/services.py:50-54,111-115,170-172`.

| Tipo | Firma verificata |
|---|---|
| PDF | `%PDF-` |
| JPEG | `FF D8 FF` |
| PNG | `89 50 4E 47 0D 0A 1A 0A` |

Il `Content-Type` dichiarato dal client **non è mai consultato**: il MIME memorizzato è quello dedotto
dalla firma e confrontato con l'estensione dichiarata `services.py:169-172`. Se non coincidono, il
file è rifiutato con il codice `content_mismatch`. Test: `tests/test_upload.py:58,62`.

Questo blocca i polyglot più comuni (`.pdf` che è in realtà HTML, `.png` che è uno script) ma **non**
tutti: un file può essere PDF valido e insieme qualcos'altro per un parser diverso. È il motivo per
cui l'antivirus (§5) resta necessario.

### 3.4 Verifiche specifiche per tipo

| Tipo | Verifica | Stato | Dove |
|---|---|---|---|
| Immagini | Pillow `Image.open()` + `verify()`, formato riletto e confrontato | **IMPLEMENTATO** | `services.py:134-147` |
| Immagini | Guardia contro la bomba di decompressione (`DecompressionBombWarning` promosso a errore) | **IMPLEMENTATO** | `services.py:137-138` |
| PDF | Rifiuto se compaiono `/JavaScript`, `/JS` o `/Launch` nei primi 2 MB | **IMPLEMENTATO** | `services.py:56,150-155` |
| PDF | Oggetti in flussi compressi, `/EmbeddedFile`, `/OpenAction`, `/AA` | **RICHIESTO** — la scansione è testuale e non decomprime | — |
| Tutti | Ri-analisi periodica dei file conservati | **RICHIESTO** | — |

### 3.5 Dimensione

**IMPLEMENTATO** — `apps/documents/services.py:42,160-164`: minimo 1 byte (`empty`), massimo
**10 MB** (`too_large`). Vincolo di integrità anche in database:
`CheckConstraint(size > 0)` `apps/documents/models.py:95`.

### 3.6 Nome del file e path traversal

**IMPLEMENTATO** — `sanitise_filename` `apps/documents/services.py:91-103`:

1. si prende **solo il basename**, interpretando sia i separatori POSIX sia quelli Windows
   (`PureWindowsPath(PurePosixPath(name).name).name`) — `../../etc/passwd`, `..\\..\\boot.ini` e
   `C:\Users\x\doc.pdf` collassano tutti sul nome finale;
2. normalizzazione Unicode NFKC (contro gli omoglifi e le forme composte);
3. rimozione dei caratteri di controllo (compreso `\x00`);
4. sostituzione di tutto ciò che non è `\w`, `.`, `-` o spazio con `_`;
5. troncamento a 100 caratteri di radice, estensione in minuscolo;
6. se non resta nulla: `document`.

Il nome così ottenuto è **solo un'etichetta** mostrata all'utente (`original_name`): **non viene mai
usato per costruire il percorso su disco** (§4). Il doppio controllo è voluto: anche se la
sanificazione avesse un difetto, non esiste un percorso in cui il nome dell'utente tocchi il
filesystem. Test: `tests/test_upload.py:108`.

### 3.7 Hash di integrità

**IMPLEMENTATO** — SHA-256 calcolato a blocchi `services.py:125-131`, memorizzato in
`PrivateDocument.sha256` (indicizzato) `apps/documents/models.py:68`.

Usi previsti: verifica che il file restituito sia quello caricato; rilevazione di duplicati;
correlazione senza leggere il contenuto; prova di integrità in caso di contestazione.

**RICHIESTO**: verifica dell'hash **alla consegna** (oggi il file viene aperto e trasmesso senza
riconfronto) e comando di verifica periodica dell'integrità dell'archivio.

---

## 4. Storage

| Proprietà | Stato | Dove |
|---|---|---|
| Directory **fuori** da `MEDIA_ROOT` e dal web root | **IMPLEMENTATO** | `settings.PRIVATE_MEDIA_ROOT` `config/settings/base.py:228`; `private_root()` **solleva `ImproperlyConfigured`** se la radice privata è dentro `MEDIA_ROOT` `apps/documents/storage.py:22-27` (test `tests/test_upload.py:136`) |
| Nessuna URL pubblica possibile | **IMPLEMENTATO** | `PrivateFileSystemStorage.url()` solleva sempre `ImproperlyConfigured` `storage.py:17-19`; `base_url=None` `:33` |
| Nessun `FileField` sul modello | **IMPLEMENTATO** | scelta esplicita documentata `apps/documents/models.py:1-6`: nessun template può stampare una URL di un file privato |
| Chiave di storage non prevedibile | **IMPLEMENTATO** | `uuid4().hex` + estensione sicura `services.py:249`; nome unico in database `models.py:65` (test `tests/test_upload.py:112,130`) |
| Una directory per proprietario | **IMPLEMENTATO** | `<owner_id>/<stored_name>` `models.py:100-103`, `services.py:250` |
| Permessi di file restrittivi | **IMPLEMENTATO** | `file_permissions_mode=0o600` `storage.py:33` (efficace su POSIX; su Windows dipende dalle ACL) |
| `/media/` servito da Django solo in DEBUG | **IMPLEMENTATO** | `config/urls.py:56-57` |
| Il proxy non serve `PRIVATE_MEDIA_ROOT` | **RICHIESTO — verifica di deploy** | Ipotesi A-03 del threat model: da verificare e mettere per iscritto in `docs/DEPLOYMENT.md` |
| Cifratura a riposo | **RICHIESTO** | A livello di volume, a carico dell'hosting (CR-08, REQ-SEC-03) |
| Storage a oggetti con URL firmate | **DESIGN ONLY** | Se si passerà a S3-compatibile: bucket privato, nessun ACL pubblico, URL firmate a scadenza breve |

---

## 5. Analisi antivirus

### 5.1 Il punto di integrazione

**IMPLEMENTATO come punto di estensione, non come protezione.**

```python
# apps/documents/services.py:189-207
def scan_file(path: str) -> str:
    dotted = getattr(settings, "DOCUMENT_SCANNER", "") or ""
    if not dotted:
        return ScanStatus.PENDING        # nessuno scanner configurato
    ...
    except Exception:
        log.exception("document scanner failed")
        return ScanStatus.ERROR          # un errore non diventa MAI "clean"
    if result not in ScanStatus.values:
        return ScanStatus.ERROR          # una risposta sconosciuta non diventa MAI "clean"
```

Proprietà importanti, tutte verificate: un fallimento dello scanner produce `error`, mai `clean`
`:201-203`; una risposta non riconosciuta produce `error` `:204-206`; lo scanner è chiamato in modo
sincrono all'upload `services.py:253`; un file `infected` viene **cancellato dal disco** subito,
mantenendo la riga `services.py:269-271,214-216`.

Configurazione: `DOCUMENT_SCANNER` = percorso puntato di un callable `(path) -> str`
`config/settings/base.py:348`. Comando di ripasso: `documents_scan_pending`
(`services.run_pending_scans` `:227-235`).

### 5.2 Gli stati dell'analisi

| Stato | Significato | Effetto sul download | Dove |
|---|---|---|---|
| `pending` | Nessuno scanner configurato, oppure non ancora analizzato | Scaricabile **solo dal proprietario** `apps/documents/views.py:102-104` | `models.py:27-28` |
| `clean` | Analizzato e sano | Scaricabile da chi la policy autorizza | `models.py:28` |
| `infected` | Malevolo | **Mai scaricabile**, file rimosso dal disco | `views.py:100-101`, `services.py:214-216` |
| `error` | Analisi fallita | Come `pending`: solo il proprietario | `models.py:30` |

### 5.3 La lacuna

`DOCUMENT_SCANNER` è **vuoto per difetto** `config/settings/base.py:348` e nessun motore è installato
(`docs/SECURITY.md` §12). In questo stato:

- ogni file resta `pending` e **è scaricabile dal proprietario**;
- un `role:staff`/`role:administrator` **non** può scaricarlo (solo `clean`), il che è corretto ma
  significa che l'unico modo per rendere `clean` un documento è la **revisione manuale** dal
  back-office `apps/documents/admin.py:119-125`, tracciata con `documents.scan_result`;
- il rischio residuo è basso per il server (il file non è mai eseguito né renderizzato) e reale per
  **la postazione di chi lo apre**.

**RICHIESTO prima dell'apertura al pubblico dei documenti**: un motore reale (ClamAV o servizio
equivalente nello SEE) dietro `DOCUMENT_SCANNER`; analisi asincrona con stato visibile all'utente;
finestra massima in `pending` oltre la quale il download è sospeso anche per il proprietario;
ri-analisi periodica con le firme aggiornate.

---

## 6. Autorizzazione all'accesso

### 6.1 Lettura della lista

**IMPLEMENTATO** — la lista parte da una queryset già filtrata:
`PrivateDocument.objects.for_owner(request.user)` `apps/documents/views.py:43`, che combina «non
cancellato» e «di proprietà» `apps/documents/models.py:33-41`. Nessun filtro applicato dopo la
lettura, nessun conteggio su righe altrui (test `tests/test_download.py:127`).

### 6.2 Policy a livello di oggetto

**IMPLEMENTATO** — `apps/documents/policies.py:26-38`:

| Azione | Chi |
|---|---|
| `view`, `download` | il proprietario · il **responsabile** (`MembershipRole.OWNER`) dell'organizzazione indicata sul documento · `role:staff` · `role:administrator` |
| `delete` | **solo il proprietario** |
| qualsiasi azione su un documento cancellato | nessuno (`deleted_at is not None` → `False` `:28-29`) |

`superadmin` passa prima della policy `apps/accounts/permissions.py:39-40`. Un semplice **membro**
dell'organizzazione non basta: serve il ruolo `OWNER` `policies.py:20-23` (test
`tests/test_download.py:95`). `role:moderator` e il solo flag `is_staff` non aprono nulla (test
`:84`).

**RICHIESTO** quando il fascicolo entrerà in servizio: estendere la policy alle assegnazioni vive
(professionista, operatore, attore autorizzato) e alla relazione documento ↔ `ChecklistItem`, con lo
stesso predicato `is_live` usato da `cases` (`PERMISSION_MODEL.md` §4.2).

---

## 7. Download

```python
# apps/documents/views.py:94-115
@login_required
@never_cache
@require_http_methods(["GET", "HEAD"])
def download(request, pk):
    doc = get_object_or_404(PrivateDocument.objects.alive().select_related("owner"), pk=pk)
    require(request.user, "download", doc)                  # autorizzazione a OGNI download
    if doc.is_infected or not doc.has_file:
        raise PermissionDenied
    if not doc.is_clean and doc.owner_id != request.user.id:
        raise PermissionDenied                              # pending/error: solo il proprietario
    response = FileResponse(..., as_attachment=True, filename=doc.original_name,
                            content_type=doc.content_type)
    response["X-Content-Type-Options"] = "nosniff"
    response["Cache-Control"] = "private, no-store"
    response["Content-Security-Policy"] = "default-src 'none'; sandbox"
    record(request, action="documents.downloaded", target=doc, metadata={"scan_status": doc.scan_status})
    return response
```

| Controllo | Stato | Perché |
|---|---|---|
| Autenticazione | **IMPLEMENTATO** `:94` | — |
| **Autorizzazione a ogni download** | **IMPLEMENTATO** `:99` | Nessun link «già autorizzato»: il controllo si rifà ogni volta |
| Documenti cancellati esclusi dalla query | **IMPLEMENTATO** `:98` | — |
| File infetti mai serviti | **IMPLEMENTATO** `:100-101` | — |
| `pending`/`error` solo al proprietario | **IMPLEMENTATO** `:102-104` | Riduce il contagio fra utenti |
| `Content-Disposition: attachment` | **IMPLEMENTATO** `:107` (`as_attachment=True`) | Il browser **scarica**, non renderizza: neutralizza l'HTML/SVG che fosse sfuggito |
| `X-Content-Type-Options: nosniff` | **IMPLEMENTATO** `:111` | Impedisce al browser di reinterpretare il tipo |
| `Content-Type` dal **valore verificato**, non dal client | **IMPLEMENTATO** `:109` (`doc.content_type`, scritto dalla validazione) | — |
| `Cache-Control: private, no-store` | **IMPLEMENTATO** `:112` | Nessuna copia in cache condivisa o su disco del browser |
| `Content-Security-Policy: default-src 'none'; sandbox` sulla risposta del file | **IMPLEMENTATO** `:113` | Difesa in profondità se il file venisse comunque aperto in un contesto di documento |
| `X-Frame-Options: DENY` | **IMPLEMENTATO** globale `config/settings/base.py:306` | — |
| `@never_cache` sulla vista | **IMPLEMENTATO** `:95` | — |
| Solo `GET`/`HEAD` | **IMPLEMENTATO** `:96` | — |
| **Evento di audit** a ogni download | **IMPLEMENTATO** `:114` | `documents.downloaded` con lo stato di analisi |
| `Content-Length` corretto e range non supportati | **IMPLEMENTATO** (`FileResponse` standard) | — |
| **URL temporanee firmate** | **RICHIESTO** (REQ-DOC-02) | §7.1 |
| Limite di frequenza sul download | **RICHIESTO** | Un account compromesso può scaricare tutto senza allerta (T-10) |
| Filigrana / tracciamento della copia | **DESIGN ONLY** | Da valutare per i documenti condivisi con un attore autorizzato |

### 7.1 URL temporanee firmate — specifica del controllo mancante

REQ-DOC-02 chiede «URL temporanei firmati dove applicabile». Oggi **non esistono**. Quando serviranno
(consegna a un revisore esterno, anteprima in un'applicazione, storage a oggetti), valgono queste
regole:

1. il token firma **utente + documento + scopo + scadenza**, mai il solo documento;
2. scadenza breve (ordine dei minuti) e **monouso** dove possibile;
3. firmato con `SECRET_KEY` tramite `django.core.signing`, mai un hash artigianale;
4. **si aggiunge alla policy, non la sostituisce**: la vista ricalcola comunque `require(...)`;
5. la revoca dell'accesso (assegnazione revocata, consenso ritirato, documento cancellato) prevale
   sul token ancora valido;
6. l'emissione e l'uso del token sono due eventi di audit distinti
   (`documents.link_issued`, `documents.downloaded`).

---

## 8. Stati visibili all'utente

`PLATFORM_REQUIREMENTS_V2.md` §7 prescrive sette stati. **Nessuno di essi esiste nel modello dati
oggi**: `PrivateDocument` ha solo `scan_status` (tecnico) e i flag `deleted_at` / `file_removed_at`.
REQ-DOC-04 è correttamente `TODO`.

| Stato richiesto | Significato | Origine | Stato |
|---|---|---|---|
| **MANCANTE** | Un requisito della checklist esige un documento che non è stato caricato | `ChecklistItem` senza `Document` collegato | **RICHIESTO** — dipende dal fascicolo |
| **CARICATO** | Ricevuto, non ancora esaminato | Upload riuscito | **PARZIALE** — oggi corrisponde a `scan_status = pending/clean` |
| **IN REVISIONE** | Un attore responsabile lo sta esaminando | Presa in carico da un assegnatario | **RICHIESTO** |
| **VALIDO** | Accettato per il requisito a cui è collegato | Decisione di un attore competente | **RICHIESTO** |
| **NON VALIDO** | Rifiutato, con motivo | Decisione di un attore competente | **RICHIESTO** |
| **SCADUTO** | La validità del documento è terminata | `expires_on` superata | **RICHIESTO** — il campo non esiste (`retention_until` è la *conservazione*, non la *validità*) |
| **DA SOSTITUIRE** | Serve una nuova versione | Rifiuto o scadenza | **RICHIESTO** |

### 8.1 Come vanno costruiti

- `DocumentStatus` è una **macchina a stati separata** da `ScanStatus`: uno stato tecnico
  (`pending/clean/infected/error`) e uno stato di dominio (i sette qui sopra) non devono mai essere
  lo stesso campo. Un file `clean` può essere `NON VALIDO`; un file `pending` non può essere `VALIDO`.
- Ogni transizione di dominio passa da un servizio, registra **chi** l'ha decisa, **quando** e **perché**, e
  genera un `AuditEvent` (`documents.status_changed`).
- Solo chi ha la responsabilità sul `ChecklistItem` collegato può portare a `VALIDO`/`NON VALIDO`:
  la persona **non** può dichiarare valido il proprio documento (stessa logica di
  `apps/cases/policies.py:77-80`).
- `SCADUTO` è calcolato da `expires_on`, non impostato a mano; un comando pianificato lo applica e
  notifica, con evento di audit.
- `DA SOSTITUIRE` genera un `ChecklistItem` aperto con attore responsabile e scadenza.

---

## 9. Versioni e sostituzione

**RICHIESTO** (REQ-DOC-05, `TODO`). Oggi un nuovo caricamento crea una riga indipendente: non esiste
un legame «versione 2 del passaporto».

Specifica minima:

- `Document` (logico) ↔ `DocumentVersion` (file), con `version` crescente e una sola versione corrente;
- le versioni precedenti **non si cancellano** quando una nuova è accettata: restano fino alla
  scadenza della conservazione, perché una decisione passata è stata presa su quella versione;
- ogni versione ha il proprio hash, il proprio stato di analisi e la propria cronologia;
- la cronologia dei caricamenti è visibile al titolare e agli attori autorizzati;
- la sostituzione genera `documents.version_added` e, se collegata a un requisito, aggiorna il
  `ChecklistItem`.

---

## 10. Cancellazione, conservazione, purga

| Operazione | Che cosa fa | Stato | Dove |
|---|---|---|---|
| **Soft delete** | `deleted_at` valorizzato, la riga sparisce da ogni lista e la policy nega tutto | **IMPLEMENTATO** | `services.soft_delete` `:296-301`; policy `:28-29`; audit `documents.deleted` |
| **Purga** | Il file è rimosso dal disco, `original_name` diventa `"purged"`, la descrizione è svuotata, **la riga resta come tombstone** | **IMPLEMENTATO** | `services.purge_document` `:304-319`; audit `documents.purged` |
| **Purga per conservazione** | File con `retention_until` superata + file di righe soft-deleted | **IMPLEMENTATO**, **dry-run per difetto** | `services.purge_expired` `:322-333`; comando `documents_purge_expired` (richiede `--apply`) |
| **Anonimizzazione dell'account** | Tutti i file della persona sono purgati | **IMPLEMENTATO** | segnale `user_anonymised` → `purge_user_documents` `apps/documents/receivers.py:12-15`, `services.py:336-342` |
| **Hard delete della riga** | Il file viene rimosso dal disco dal segnale `post_delete` | **IMPLEMENTATO** (difensivo) | `receivers.py:18-22` |
| **`retention_until` popolata automaticamente** | — | **RICHIESTO**: oggi il campo è impostabile a mano, nessuna regola lo valorizza | `models.py:78-83` |
| **Durata di conservazione per tipo di documento** | — | **RICHIESTO**: dipende dalla policy del titolare (`DATA_CLASSIFICATION.md` §6.2, CR-12) | — |
| **Certificato di cancellazione** | — | **DESIGN ONLY**: prova esportabile su richiesta dell'interessato | — |

Il **tombstone** è una scelta deliberata: la riga senza contenuto conserva `id`, `sha256`, `size`,
`created_at` e la cronologia di audit, così una domanda futura («esisteva un documento? quando è
stato cancellato?») ha risposta, senza che il dato personale sopravviva.

---

## 11. Back-office

| Proprietà | Stato | Dove |
|---|---|---|
| Elenco in sola lettura: tutti i campi readonly | **IMPLEMENTATO** | `apps/documents/admin.py:75` |
| Nessuna creazione, nessuna cancellazione dall'admin | **IMPLEMENTATO** | `:113-117` |
| Link di download visibile **solo al superutente** | **IMPLEMENTATO** | `:95-111`; il link porta comunque alla vista autorizzata `:93` |
| Revisione manuale «sano / infetto» tracciata | **IMPLEMENTATO** | `:119-133` → `apply_scan_result` → audit `documents.scan_result` |
| `role:administrator` ha solo `documents: view` | **IMPLEMENTATO** | `apps/accounts/roles.py:75` |
| Export CSV dei **soli metadati** (nessun contenuto) | **IMPLEMENTATO** | `:135-157` |
| **L'export CSV non genera un evento di audit** | **LACUNA** | `:135-157` — a differenza di `enquiries.export_csv`. L'export contiene e-mail dei proprietari e nomi dei file: va tracciato |
| Ricerca per `owner__email`, `original_name`, `sha256` | **IMPLEMENTATO** | `:72` — attenzione: è una superficie di ricerca su dati personali riservata al back-office |

---

## 12. Riepilogo: implementato / richiesto

| # | Elemento | Stato |
|---|---|---|
| 1 | Allowlist di estensioni e MIME (pdf, jpg, jpeg, png) | **IMPLEMENTATO** |
| 2 | Rifiuto di SVG, HTML, Office, eseguibili, archivi | **IMPLEMENTATO** (per allowlist) |
| 3 | Verifica dei magic bytes contro l'estensione | **IMPLEMENTATO** |
| 4 | `Content-Type` del client ignorato | **IMPLEMENTATO** |
| 5 | Verifica Pillow + guardia anti-bomba per le immagini | **IMPLEMENTATO** |
| 6 | Rifiuto dei PDF con contenuto attivo (testuale) | **IMPLEMENTATO** |
| 7 | Analisi dei PDF con flussi compressi | **RICHIESTO** |
| 8 | Limite di dimensione 1 B – 10 MB | **IMPLEMENTATO** |
| 9 | Limite di frequenza sull'upload | **IMPLEMENTATO** |
| 10 | Sanificazione del nome + immunità al path traversal | **IMPLEMENTATO** |
| 11 | Chiave di storage non prevedibile (uuid4) | **IMPLEMENTATO** |
| 12 | Storage fuori dal web root, nessuna URL pubblica | **IMPLEMENTATO** |
| 13 | Hash SHA-256 di integrità | **IMPLEMENTATO** (verifica alla consegna: **RICHIESTO**) |
| 14 | Punto di integrazione antivirus con quattro stati | **IMPLEMENTATO** |
| 15 | Motore antivirus reale | **RICHIESTO** |
| 16 | Autorizzazione a ogni download | **IMPLEMENTATO** |
| 17 | `Content-Disposition: attachment` + `nosniff` + `no-store` + CSP sulla risposta | **IMPLEMENTATO** |
| 18 | Evento di audit a ogni download | **IMPLEMENTATO** |
| 19 | URL temporanee firmate | **RICHIESTO** |
| 20 | Limite di frequenza / allerta sui download di massa | **RICHIESTO** |
| 21 | Sette stati di dominio (MANCANTE → DA SOSTITUIRE) | **RICHIESTO** |
| 22 | Versionamento e cronologia dei caricamenti | **RICHIESTO** |
| 23 | Scadenza di validità (`expires_on`) distinta dalla conservazione | **RICHIESTO** |
| 24 | Soft delete, purga, tombstone, anonimizzazione | **IMPLEMENTATO** |
| 25 | `retention_until` valorizzata da una policy per finalità | **RICHIESTO** |
| 26 | Collegamento documento ↔ requisito ↔ fascicolo | **RICHIESTO** |
| 27 | Accesso di professionisti e attori autorizzati per assegnazione | **RICHIESTO** |
| 28 | Audit dell'export CSV di back-office | **RICHIESTO** |
| 29 | Validazione equivalente per i media pubblici del CMS (`cms.MediaAsset`) | **RICHIESTO** (T-11) |

**Le tre cose da fare per prime**: (15) l'antivirus reale, (21-23) gli stati di dominio con scadenza
e versioni, (27) l'accesso per assegnazione con lo stesso predicato `is_live` del fascicolo.

---

Classificazione di questo documento: **interno**
(`docs/source-of-truth/CONFIDENTIALITY_REGISTER.md` §2).
