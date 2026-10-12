# SCANSIONE DELLA CRONOLOGIA — DOPO LA RISCRITTURA

21 settembre 2026 · `scripts/history_secret_scan.py` · Cronologia risultante, **ogni blob
raggiungibile da ogni ref**

Riferimento: `docs/security/HISTORY_REWRITE_2026-09-21.md` §6.

---

## 1. Esito

| Misura | Prima | Dopo |
|---|---:|---:|
| HEAD | `53d9b46` | **`8d8058d`** |
| Commit | 65 | 69 |
| Blob in cronologia | 2124 | 2131 |
| Blob di testo scansionati | 1311 | 1323 |
| Blob binari | 171 | **155** |
| Dimensione di `.git` | 35 MB | **20 MB** |
| **Indirizzi e-mail di terzi** | **2** | **0** |
| Documenti sorgente del committente | 4 file, ogni versione | **0** |
| Screenshot committati per errore | 14 | **0** |

`git fsck` non riporta nulla.

I quattro commit in più non sono un errore di conteggio: sono la bonifica stessa, che è stata
committata prima di riscrivere — la guardia per forma, l'uscita dei documenti sorgente, la tabella
di redazione esterna e l'ottimizzazione dello strumento.

---

## 2. I 285 rilievi residui, uno per uno

Il totale è più alto di prima (269 → 285) e questo è previsto: i documenti scritti *durante* la
bonifica citano gli esempi sintetici che la bonifica ha deciso di **lasciare**, e lo scanner li
rileva come rileverebbe qualunque altra stringa della stessa forma.

| Pattern | N | Verdetto | Che cos'è davvero |
|---|---:|---|---|
| `hex64` | 140 | **atteso** | Digest d'integrità di `apps/cms/locked_content.sha256.json` e di `tests/security/test_confidential_material.py`. L'unico che era un dato personale non c'è più |
| `db_url_pw` | 86 | **atteso** | `postgres://ile:ile-dev-password@…`, password del database di sviluppo locale, dichiarata in `.env.example`. `prod.py` esige `DATABASE_URL` dall'ambiente |
| `secret_assign` | 28 | **atteso** | Password sintetiche di fixture su account `@example.test`, più `SECRET_KEY` di `config/settings/test.py`, che si chiama `test-only-secret-key-not-for-production` |
| `phone_intl` | 27 | **atteso** | Numeri sintetici: `+212600000000`, `+39 049 0000000`, `+39 0000 000000`. Sei dei ventisette sono nel documento della riscrittura, che li cita come esempi di ciò che è stato lasciato |
| `id_document` | 4 | **atteso** | Tre occorrenze dell'etichetta d'interfaccia «numero di passaporto» e una del pattern `CNIE` dentro lo scanner stesso |
| **`email`** | **0** | — | |
| `aws_key`, `private_key`, `gh_token`, `slack_token`, `google_key`, `stripe_key`, `jwt`, `codice_fiscale`, `iban` | 0 | — | Nessuna occorrenza, né prima né dopo |

**Nessun rilievo residuo è un dato personale di un terzo, una credenziale di produzione o un
documento riservato.**

---

## 3. I 155 blob binari

Non sono stati grepati, perché una regex su un PNG non dimostra nulla in nessuna delle due
direzioni. Sono stati trattati per percorso, e i 26 screenshot del sito di produzione sono stati
**guardati**: sono la homepage pubblica di marketing, senza dati personali.

| Directory | Blob | Contenuto |
|---|---:|---|
| `static/img/photos` | 73 | Immagini del sito, licenze in `docs/IMAGE_LICENSES.md` |
| `static/fonts` | 38 | Caratteri tipografici serviti localmente — mai da una CDN esterna |
| `docs/audit/current-site/screenshots` | 26 | Catture della homepage pubblica di produzione |
| `locale/*/LC_MESSAGES` | 16 | Cataloghi compilati |
| `docs/qa/lighthouse` | 1 | Traccia di performance. Verificata: unico host `127.0.0.1`, nessun indirizzo, nessun percorso utente |
| `static/img` | 1 | |

I 16 blob binari in meno rispetto a prima sono i due PDF sorgente e i quattordici screenshot
committati per errore.

---

## 4. Che cosa questa scansione **non** dimostra

Va detto, altrimenti il documento vale meno di quanto sembri.

1. **Non dimostra che i valori non siano mai usciti.** La cronologia è pulita da oggi; il
   repository non ha mai avuto un remote e non è mai stato pubblicato, ed è questo — non la
   scansione — a rendere improbabile che siano usciti.
2. **Non dimostra che il bundle probatorio sia al sicuro.** Il bundle contiene tutto ciò che è
   stato rimosso, per costruzione. Vive fuori dal repository con le sue regole scritte.
3. **Non copre i dati dentro le immagini.** Se uno screenshot contenesse un indirizzo visibile nei
   pixel, questa scansione non lo vedrebbe. I 26 screenshot esistenti sono stati guardati; il
   prossimo va guardato.
4. **Non è un controllo continuo.** È una fotografia. La guardia che vale ogni giorno è
   `tests/compliance/test_no_personal_data_in_repository.py`, che sorveglia la working tree; la
   cronologia va riscansionata prima di aggiungere un remote.

---

## 5. Come rieseguirla

```bash
.venv/Scripts/python.exe scripts/history_secret_scan.py rapporto.json
```

Legge `git rev-list --objects --all`, non `git ls-files`. La differenza è tutto il punto: la
working tree mostra un commit, la cronologia mostra ogni blob mai esistito, compresi quelli il cui
percorso è stato cancellato.
