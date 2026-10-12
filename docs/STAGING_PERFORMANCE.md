# PRESTAZIONI — MISURA SU AMBIENTE SIMIL-PRODUZIONE

21 settembre 2026 · **Staging, non produzione** · Nessun deploy eseguito

> `docs/FINAL_REPORT.md` §13 riportava numeri presi da `runserver` con `DEBUG=1`. Non erano numeri
> di produzione e lo dicevano, ma erano anche inutili: il server di sviluppo è monoprocesso, serve
> i file statici senza compressione né cache, e ricarica i template a ogni richiesta. Misurarlo
> risponde a una domanda che nessuno ha.
>
> Questo documento sostituisce quella misura con una presa su uno stack che assomiglia alla
> produzione — e continua a **non** essere produzione, per le ragioni elencate al §2.

---

## 1. Che cosa è stato misurato

| Componente | Staging | `runserver` (la misura precedente) |
|---|---|---|
| Sistema operativo | Linux (container `python:3.13-slim`) | Windows |
| Server applicativo | **gunicorn, 3 worker** | server di sviluppo Django, monoprocesso |
| `DEBUG` | **False** | True |
| File statici | **whitenoise**, `CompressedManifestStaticFilesStorage` | serviti da Django, senza cache |
| Impostazioni | `config.settings.prod` | `config.settings.dev` |
| Database | PostgreSQL 17, container dedicato | PostgreSQL 17 condiviso |
| Intestazioni di sicurezza | **attive** | parziali |
| Secondo fattore | **imposto** | spento |

Avviabile con:

```bash
docker compose -f docker-compose.staging.yml --profile staging up -d --build
```

`DJANGO_SECRET_KEY` e `POSTGRES_PASSWORD` devono essere nell'ambiente (o in un `.env` accanto al
file, ignorato da git): il file non contiene alcun valore e, se una delle due manca,
`docker compose` si rifiuta di partire dicendo quale.

`docker-compose.staging.yml` è **autonomo**: non estende `docker-compose.yml` e ha il proprio
database. La prima versione puntava al servizio `db` condiviso, e `docker compose --profile staging
up` lo ha ricreato — chiudendo ogni connessione aperta e facendo fallire una corsia di pytest già
in esecuzione con «terminating connection due to administrator command». Uno stack di staging che
può buttare giù il database di sviluppo non è uno stack di staging.

---

## 2. Perché NON è produzione

Va letto prima dei numeri, non dopo.

1. **Un solo host.** Niente terminazione TLS davanti, niente bilanciatore, niente CDN.
2. **Loopback.** Nessuna latenza di rete reale, nessuna perdita di pacchetti, nessun handshake TLS.
   Il pubblico di questa piattaforma accede da rete mobile marocchina: la differenza non è del
   dieci per cento.
3. **Il browser gira sulla stessa macchina del server.** Competono per la stessa CPU, il che
   peggiora i tempi di rendering e migliora quelli di rete, in misura non separabile.
4. **`SECURE_SSL_REDIRECT` e HSTS sono spenti**, con `ILE_ALLOW_INSECURE_PROD=1`, perché non c'è
   TLS davanti. È l'unica volta in cui quella scappatoia è usata, ed è scritta nel compose.
5. **Contenuti sintetici, nessuna regola in vigore.** Le pagine misurate non toccano il rule engine.
6. **Nessun carico.** Una richiesta alla volta. Non è un test di carico e non lo sostituisce.

---

## 3. Misure

Otto pagine pubbliche, due viewport, browser Chromium. Tempo di risposta al socket = mediana di
cinque richieste senza browser, così il tempo del server e quello del rendering restano distinti.

| Pagina | Viewport | Server (ms) | TTFB | FCP | LCP | CLS | kB | Richieste |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| home FR | mobile | 41,7 | 57 | — | — | 0,0000 | 425,5 | 19 |
| home FR | desktop | 41,7 | 48 | 272 | 272 | 0,0001 | 425,5 | 19 |
| home AR | mobile | 33,1 | **491** | 712 | 712 | 0,0001 | 384,2 | 22 |
| home AR | desktop | 33,1 | 41 | 312 | 312 | 0,0046 | 384,2 | 22 |
| progetto FR | mobile | 18,9 | 21 | 172 | 172 | 0,0000 | 271,0 | 17 |
| progetto FR | desktop | 18,9 | 21 | 188 | 188 | 0,0000 | 271,0 | 17 |
| imprese FR | mobile | 27,7 | 32 | 196 | 196 | 0,0000 | 270,5 | 17 |
| imprese FR | desktop | 27,7 | 25 | 196 | 196 | 0,0000 | 270,5 | 17 |
| rete FR | mobile | 21,5 | 38 | 196 | 196 | 0,0000 | 271,6 | 17 |
| rete FR | desktop | 21,5 | 30 | 192 | 192 | 0,0000 | 271,6 | 17 |
| contatti FR | mobile | 18,4 | 18 | 180 | 180 | 0,0000 | 269,8 | 17 |
| contatti FR | desktop | 18,4 | 18 | 184 | 184 | 0,0000 | 269,8 | 17 |
| Forum FR | mobile | 26,6 | 24 | 188 | 188 | 0,0000 | 419,0 | 18 |
| Forum FR | desktop | 26,6 | 25 | 232 | 232 | 0,0000 | 419,0 | 18 |
| attualità FR | mobile | 23,3 | 24 | 188 | 188 | 0,0000 | 261,7 | 16 |
| attualità FR | desktop | 23,3 | 24 | 172 | 172 | 0,0000 | 261,7 | 16 |

**Peggior LCP 712 ms · peggior CLS 0,0046 · payload massimo 425 kB su 22 richieste.**

### Le due anomalie, non nascoste

**`home FR mobile` riporta FCP e LCP a zero.** Non significa «istantaneo»: significa che il
`PerformanceObserver` si è agganciato dopo che il primo disegno era già avvenuto, sulla prima
pagina visitata in assoluto. È un artefatto di misura. La riga desktop della stessa pagina, con il
browser ormai caldo, dà 272 ms, ed è il numero da leggere.

**`home AR mobile` ha un TTFB di 491 ms contro i 41 della riga desktop.** È l'avvio a freddo: la
prima richiesta in arabo carica il catalogo compilato. La seconda no. In produzione lo paga il
primo visitatore arabo dopo ogni riavvio di un worker — visibile, non grave, e sparisce con un
riscaldamento all'avvio se si decide che valga la pena.

---

## 4. File statici

Non è un dettaglio: è la differenza fra il primo e il secondo caricamento per ogni visitatore.

| Verifica | Esito |
|---|---|
| Nome con impronta del contenuto | `fonts.531f5f8c7ad5.css` |
| `Cache-Control` | `max-age=315360000, public, immutable` |
| `Vary: Accept-Encoding` | presente |
| Compressione | `Content-Encoding: gzip`, **14 336 B → 1 422 B** (−90 %) |
| `ETag` | presente |

---

## 5. Intestazioni di sicurezza sull'origine servita

Lette sulla risposta reale, non nelle impostazioni.

```
Content-Security-Policy: base-uri 'self'; style-src 'self'; form-action 'self';
  frame-ancestors 'none'; connect-src 'self'; default-src 'self';
  upgrade-insecure-requests; object-src 'none'; font-src 'self';
  img-src 'self' data:; script-src 'self'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
X-Permitted-Cross-Domain-Policies: none
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(),
  interest-cohort=()
```

Nessuno `'unsafe-inline'`, nessuno `'unsafe-eval'`, nessun host esterno in alcuna direttiva. Il
cookie di lingua esce con `HttpOnly`, `SameSite=Lax` e `Secure`.

**Manca**, e manca perché non c'è TLS davanti a questo container: `Strict-Transport-Security`. Va
verificata sull'origine reale al momento del go-live — `docs/DEPLOYMENT_READINESS.md` §8.

`Server: gunicorn` è esposto. Non rivela la versione, ma il proxy di produzione dovrebbe toglierlo.

---

## 6. Perché non Lighthouse

La direttiva chiede Core Web Vitals o Lighthouse. Qui ci sono i **Core Web Vitals misurati** —
LCP, CLS, FCP e TTFB dal `PerformanceObserver` del browser — e non un punteggio Lighthouse.

Un punteggio Lighthouse preso su loopback, dalla stessa macchina che esegue il server, con la
simulazione di rete che Lighthouse applica sopra una latenza già nulla, è un numero su questo
portatile. I valori grezzi almeno dicono che cosa hanno misurato. Quando esisterà un'origine vera
con TLS e un profilo di rete realistico, Lighthouse avrà senso ed è nella checklist di go-live.

---

## 7. Che cosa questa misura NON dice

1. **Come si comporta sotto carico.** Una richiesta alla volta.
2. **Come si comporta su rete mobile marocchina.** Il pubblico reale, la condizione reale.
3. **Come si comportano le pagine autenticate.** Misurate solo le pubbliche.
4. **Se il rule engine è veloce.** Nessuna regola era in vigore durante la misura.
5. **Se 37 query sul cruscotto sono troppe.** Resta il rilievo aperto di `FINAL_REPORT` §15.
