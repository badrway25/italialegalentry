# DEPLOYMENT READINESS — preparazione, **nessun deploy eseguito**

Stato: preparatorio · 21 settembre 2026 · Nessun remote, nessun DNS, nessuna infrastruttura toccata

> Questo documento prepara. Non esegue. `docs/DEPLOYMENT.md` resta la procedura operativa; qui c'è
> l'inventario di ciò che deve esistere **prima** che quella procedura abbia senso, e le cose che
> sono state verificate eseguendole in locale.

---

## 1. Matrice degli ambienti

| | `dev` | `test` | `staging` | `prod` |
|---|---|---|---|---|
| Modulo | `config.settings.dev` | `config.settings.test` | `config.settings.prod` | `config.settings.prod` |
| `DEBUG` | 1 | 0 | **0** | **0** |
| TLS | no | n/d | **sì** | **sì** |
| `SECURE_SSL_REDIRECT` | — | — | true | true |
| HSTS | — | — | 31536000 | 31536000 |
| `BACKOFFICE_MFA_ENFORCED` | 0 | 0 | **1** | **1** |
| `ILE_SEED_DEMONSTRATION_DATA` | `DEBUG` | **pinned false** | **false** | **pinned false** |
| Dati | sintetici | sintetici | **sintetici** | reali |
| E-mail | console | locmem | **console o casella di prova** | SMTP |
| Cache | locmem | locmem | Redis o locmem | Redis consigliato |

**Staging non riceve dati reali.** Il Technical Blueprint §13 e la Relazione Tecnica §11 lo dicono
con la stessa frase, e la vecchia piattaforma è il motivo per cui vale la pena ripeterlo.

---

## 2. Inventario delle variabili d'ambiente

28 variabili sono lette dalle impostazioni. Ricavate dal codice, non dalla memoria:

```bash
.venv/Scripts/python.exe -c "import re,pathlib; \
  src=pathlib.Path('config/settings/base.py').read_text(encoding='utf-8')+pathlib.Path('config/settings/prod.py').read_text(encoding='utf-8'); \
  print('\n'.join(sorted(set(re.findall(r'env(?:\.\w+)?\(\s*[\"\x27]([A-Z_][A-Z0-9_]*)[\"\x27]', src)))))"
```

### 2.1 Segreti — mai nel repository, mai in un log, mai in un ticket

| Variabile | Che cos'è | Rotazione |
|---|---|---|
| `DJANGO_SECRET_KEY` | Firma sessioni, token CSRF, link firmati dei documenti | Alla compromissione. **Ruotarla invalida sessioni e link firmati in corso**: è l'effetto voluto, ma va fatto in finestra |
| `DATABASE_URL` | Contiene la password del database | Alla compromissione e all'uscita di chi la conosceva |
| `EMAIL_HOST_PASSWORD` | SMTP | Idem |
| `IP_HASH_SALT` | Sale per gli indirizzi IP nei log d'audit | **Non ruotare senza decisione**: ruotandolo, gli hash prima e dopo non sono più confrontabili e la continuità dell'audit si spezza |

`prod.py` non accetta una `DJANGO_SECRET_KEY` più corta di 50 caratteri o con meno di 5 caratteri
distinti: **si rifiuta di avviarsi**. Verificato eseguendolo.

### 2.2 Obbligatorie in produzione, senza default

| Variabile | Se manca |
|---|---|
| `DJANGO_SECRET_KEY` | `ImproperlyConfigured` all'avvio |
| `DJANGO_ALLOWED_HOSTS` | `ImproperlyConfigured` all'avvio |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `ImproperlyConfigured` all'avvio |

> **Difetto trovato preparando questo documento.** `DJANGO_CSRF_TRUSTED_ORIGINS` è obbligatoria in
> produzione e **non era in `.env.example`**. Il primo `manage.py check --deploy` con le
> impostazioni di produzione è morto proprio lì. Un `.env.example` che non elenca una variabile
> obbligatoria non è un esempio: è una trappola per chi arriva dopo. Aggiunta, insieme alle altre
> cinque che mancavano.

### 2.3 Con default, ma da dichiarare esplicitamente

`DB_CONN_MAX_AGE` · `SECURE_SSL_REDIRECT` · `SECURE_HSTS_SECONDS` · `NOTIFICATIONS_SEND_IMMEDIATELY`
· `ILE_ALLOW_INSECURE_PROD` · `REDIS_URL` · `DOCUMENT_SCANNER` · `INTEGRATIONS_TRANSPORT` ·
`PRIVATE_MEDIA_ROOT` · `ILE_VERSION_LABEL` · `ILE_REFERENCE_DATE`

`ILE_ALLOW_INSECURE_PROD=1` disattiva il controllo di coerenza TLS all'avvio. Ha un solo uso
legittimo — dietro un proxy che termina TLS su rete privata — e va messo a verbale quando si usa.

---

## 3. Hosting nell'Unione europea — checklist di verifica (CR-08, **aperto**)

Il progetto tratta dati personali di cittadini di Paesi terzi che si rivolgono ad autorità
italiane, compresi documenti d'identità. La collocazione dei dati non è un dettaglio contrattuale.

| # | Da verificare | Come si verifica davvero |
|---|---|---|
| 3.1 | Regione del server applicativo in UE/SEE | Pannello del fornitore **e** traceroute/whois dell'IP, perché la regione dichiarata e quella effettiva possono divergere |
| 3.2 | Regione del database | Idem, separatamente: applicazione e database possono stare in regioni diverse |
| 3.3 | Regione dei **backup** | È l'errore classico: applicazione in Francoforte, backup replicati fuori UE per default |
| 3.4 | Regione dello storage dei documenti privati | `PRIVATE_MEDIA_ROOT` su disco locale, oppure bucket con regione dichiarata |
| 3.5 | Regione dei log | Un servizio di log gestito è un trasferimento come un altro |
| 3.6 | Provider SMTP | Dove transitano e dove sono conservate le e-mail |
| 3.7 | CDN, se presente | Punti di presenza e cache dei contenuti |
| 3.8 | Subfornitori del fornitore | L'elenco dei sub-processor, che cambia senza preavviso |
| 3.9 | Accordo sul trattamento (art. 28 GDPR) firmato | Con l'elenco dei sub-processor allegato |
| 3.10 | Fornitore soggetto a giurisdizione extra-UE? | Una società statunitense con server a Francoforte resta soggetta al CLOUD Act. È una valutazione, non una casella |
| 3.11 | Clausole contrattuali tipo dove serve | |
| 3.12 | Registro dei trattamenti aggiornato con la collocazione reale | |

Finché 3.1–3.9 non hanno una risposta scritta, CR-08 resta aperto e il go-live non è difendibile.

---

## 4. Backup, ripristino, RPO/RTO

### 4.1 Che cosa va salvato

| Oggetto | Perché | Nota |
|---|---|---|
| Database PostgreSQL | Tutto lo stato | |
| `PRIVATE_MEDIA_ROOT` | **Documenti d'identità caricati** | Non è sotto `MEDIA_ROOT` e non è servito dal web server: un backup che copia solo `media/` lo perde in silenzio |
| Variabili d'ambiente | Senza `DJANGO_SECRET_KEY` un ripristino non apre le sessioni né i link firmati | In un gestore di segreti, non nel backup |
| Cataloghi `.mo` compilati | Rigenerabili, ma il ripristino è più veloce con essi | |

La cache è volatile. `REDIS_URL` non va salvato.

### 4.2 Proposta di RPO/RTO — da confermare dal committente

**Sono una proposta, non un impegno.** Un RPO si decide sapendo quanto costa perdere un'ora di
dati, e quella è una valutazione del committente.

| | Proposta | Perché questo numero |
|---|---|---|
| **RPO** | 24 h nominale, **1 h obiettivo** | Un dump notturno perde al massimo un giorno. Ma il dato qui è un fascicolo in preparazione per una scadenza amministrativa: rifare un caricamento di documenti è oneroso per la persona, non per il sistema. L'archiviazione continua del WAL porta l'RPO a minuti e costa poco |
| **RTO** | 4 h | Nessuna procedura amministrativa si decide in quattro ore. Un RTO più stretto costa una replica calda che questo progetto non giustifica |
| Conservazione | 30 giorni giornalieri, 12 mesi mensili | Da allineare ai termini di conservazione di `docs/PRIVACY_BY_DESIGN.md`: **un backup che sopravvive al termine di conservazione è una violazione di quel termine** |

### 4.3 Prova di ripristino — obbligatoria, e da ripetere

> **Un backup non provato non è un backup.** È l'unico punto di questa sezione che non ammette di
> essere rimandato: la prima volta che un ripristino viene provato non deve essere il giorno in cui
> serve.

Procedura minima, su una macchina che non è la produzione:

1. Prendere il backup **più recente**, non uno preparato per l'occasione.
2. Ripristinare database e `PRIVATE_MEDIA_ROOT` su un ambiente pulito.
3. `manage.py migrate --check` → nessuna migrazione in sospeso.
4. Avviare, aprire `/healthz/` → 200.
5. Aprire un fascicolo e **scaricare un documento privato**: è il passo che dimostra che il backup
   dei file e quello del database sono coerenti fra loro.
6. Verificare che una pre-valutazione si rieseguisse dallo snapshot.
7. Cronometrare, e confrontare con l'RTO dichiarato.
8. Distruggere l'ambiente di prova.

Cadenza: alla prima messa in esercizio, poi trimestrale, e dopo ogni cambio del sistema di backup.

**Già provato in questa sessione**, in piccolo: il bundle Git della cronologia è stato ripristinato
in una directory temporanea, HEAD e conteggio commit verificati, copia cancellata. È la stessa
disciplina su un oggetto più piccolo.

---

## 5. Migrazioni

### 5.1 Procedura

1. `manage.py makemigrations --check --dry-run` in integrazione continua — **ora è anche un test**,
   `tests/test_migration_drift.py`, su tutte e 28 le app. Lo era su una sola, e una deriva è passata.
2. Leggere l'SQL generato prima di applicarlo: `manage.py sqlmigrate <app> <numero>`.
3. Backup **prima**, sempre.
4. `manage.py migrate --noinput`.
5. `manage.py collectstatic --noinput`.
6. Ricaricare i processi applicativi.

### 5.2 Rollback

Il rollback di uno schema non è simmetrico al deploy e va detto chiaramente.

| Tipo di migrazione | Rollback |
|---|---|
| Additiva (nuova tabella, nuova colonna nullable) | `migrate <app> <numero precedente>`, sicuro |
| Riduttiva (colonna rimossa, tipo cambiato) | **Non reversibile senza perdita.** Si ripristina dal backup |
| Solo etichette (`choices`) | Nessun effetto sullo schema. La migrazione esiste solo per tenere pulito `makemigrations --check` |

Regola operativa: una migrazione riduttiva si spezza in due rilasci — prima smettere di usare la
colonna, poi rimuoverla in un rilascio successivo — così il rollback del codice non incontra mai uno
schema che non conosce.

---

## 6. Processi e lavori periodici

Non c'è Celery e non serve. I lavori sono comandi di gestione, da mettere in `cron` o in un timer
`systemd`.

| Comando | Cadenza proposta | Che cosa succede se non gira |
|---|---|---|
| `send_queued_emails` | ogni 5 min | Le e-mail restano in coda. Niente si perde: `EmailOutbox` è il registro |
| `notifications_scan_deadlines` | 1/giorno, di notte | Nessun avviso di scadenza. È il lavoro il cui silenzio si nota di meno |
| `documents_scan_pending` | ogni 15 min | I documenti restano «non analizzati» — che è ciò che la regola di consegna dichiara, quindi è un degrado onesto |
| `documents_purge_expired` | 1/giorno | I documenti scaduti restano oltre il termine: **è una violazione del termine di conservazione**, non un ritardo |
| `purge_expired_submissions` | 1/giorno | Idem |
| `purge_orientation_sessions` | 1/giorno | Idem |
| `deliver_outbound_events` | ogni 5 min | Integrazioni in ritardo |

I tre `purge_*` sono gli unici la cui mancata esecuzione è un problema **di conformità** e non di
servizio. Vanno monitorati come tali: l'allarme scatta se non girano, non solo se falliscono.

---

## 7. Health check, log, monitoraggio

`GET /healthz/` esegue `SELECT 1` e risponde 200, oppure 503 con `{"status":"degraded"}`.

**Che cosa non copre, e va saputo:** non verifica la raggiungibilità di `PRIVATE_MEDIA_ROOT`, non
verifica Redis, non verifica che la coda e-mail scorra. Un bilanciatore che interroga `/healthz/`
tiene in rotazione un'istanza che non riesce a servire un documento.

| Da monitorare | Soglia proposta |
|---|---|
| `/healthz/` | 3 fallimenti consecutivi |
| Tasso di 5xx | > 1 % su 5 min |
| Coda `EmailOutbox` in stato `queued` | > 50, oppure la più vecchia > 1 h |
| Lavori `purge_*` | **mancata esecuzione**, non solo fallimento |
| Spazio su `PRIVATE_MEDIA_ROOT` | < 15 % libero |
| Connessioni PostgreSQL | > 80 % di `max_connections` |
| Certificato TLS | < 21 giorni alla scadenza |
| `rules_pending_review --strict` | Uscita 1 — qualcosa è in vigore senza approvatore, o su una fonte non verificata. Oggi esce 0, perché nessuna regola è in vigore |

Il logging è strutturato in produzione (`core.logging.StructuredFormatter`) e ogni riga porta un
identificatore di richiesta. `tests/security/test_log_privacy.py` verifica che nel flusso passino
identificatori e non dati personali.

---

## 8. Intestazioni di sicurezza e CSP

Impostate dall'applicazione: `SECURE_SSL_REDIRECT`, HSTS un anno con `includeSubDomains` e
`preload`, cookie `Secure`, `X-Content-Type-Options`, `Referrer-Policy`, CSP `self` senza stili in
linea.

Da verificare **sull'origine servita**, non nelle impostazioni:

| # | Verifica |
|---|---|
| 8.1 | HSTS presente sulla risposta reale, compresi gli errori |
| 8.2 | `preload` inviato solo se si intende davvero entrare nella lista: **uscirne richiede mesi** |
| 8.3 | Nessuna intestazione duplicata fra proxy e applicazione |
| 8.4 | CSP senza violazioni in console su tutte le pagine pubbliche e riservate |
| 8.5 | Il proxy non aggiunge un `Server` con la versione |
| 8.6 | `/backoffice/` irraggiungibile dalla rete pubblica, o protetto oltre l'autenticazione |

---

## 9. DNS e cutover

| # | Passo |
|---|---|
| 9.1 | TTL abbassato a 300 s **almeno 48 ore prima** del cutover |
| 9.2 | Certificato emesso e provato **prima** di spostare il DNS |
| 9.3 | `DJANGO_ALLOWED_HOSTS` e `DJANGO_CSRF_TRUSTED_ORIGINS` contengono il dominio definitivo |
| 9.4 | Redirect da `www` a dominio nudo, o viceversa: una sola forma canonica |
| 9.5 | `robots.txt` servito dall'applicazione, non dal proxy, altrimenti i `Disallow` del back-office spariscono |
| 9.6 | I 410 e i redirect di `docs/URL_MIGRATION_MAP.md` applicati (pagina autore: 410) |
| 9.7 | `app.legalitalentry.it` — **decidere che cosa ne è**. Oggi il certificato non corrisponde e nginx risponde 503 |
| 9.8 | Piano di ritorno: TTL basso e vecchio sistema in piedi per 72 ore |

---

## 10. Che cosa manca perché questo documento diventi una procedura

1. Il fornitore di hosting non è scelto. Tutta la §3 è una checklist senza destinatario.
2. Nessun sistema di backup esiste; l'RPO/RTO della §4 è una proposta senza approvazione.
3. Nessuna prova di ripristino su dati reali — non può essercene, non ci sono dati reali.
4. Nessun monitoraggio configurato; le soglie della §7 non sono impostate da nessuna parte.
5. Nessun dominio definitivo confermato.

Nessuno dei cinque è codice. Tutti e cinque sono decisioni del committente.
