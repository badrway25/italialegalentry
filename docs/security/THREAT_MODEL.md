# THREAT MODEL — Italy Legal Entry™

Segnaposto pubblico · 9 ottobre 2026 · Requisito: **REQ-SEC-01** (`docs/source-of-truth/REQUIREMENT_MATRIX_V2.md` §M)
Perimetro: sito pubblico **e** piattaforma autenticata · Owner: referente tecnico

Il threat model completo (versione 1.0 del 20 settembre 2026: perimetro e ipotesi, asset, attori,
confini di fiducia, punti di ingresso, STRIDE per confine, catalogo delle minacce T-01…T-29,
classifica del rischio residuo e regole di manutenzione) esiste ed è mantenuto **nel registro
privato, fuori dal repository pubblico**, finché le sue voci aperte non sono chiuse nel codice e
coperte da test. Un documento che elenca le proprie lacune con la posizione nel codice è una mappa
di ciò che non è ancora corretto: si pubblica quando non lo è più.

Che cosa vale anche qui:

- la classificazione del documento è **interno** (`docs/source-of-truth/CONFIDENTIALITY_REGISTER.md`
  §2: «Threat model, classificazione dati, modello permessi — mai esposti da una vista pubblica né
  in documentazione API pubblica»); questo segnaposto è la sola parte pubblica;
- i riferimenti **T-nn** e **TB-n** nei documenti collegati (`docs/security/AUDIT_MODEL.md`,
  `DATA_CLASSIFICATION.md`, `DOCUMENT_SECURITY.md`, `PERMISSION_MODEL.md`) puntano al catalogo del
  documento privato e restano validi;
- la regola di manutenzione non cambia: il threat model si aggiorna **prima** che il codice cambi —
  nuovo modulo di dominio, nuovo ruolo, nuova integrazione esterna, primo deploy.

Rientro in questo percorso: quando ogni voce aperta del documento privato è chiusa e verificata, il
documento completo torna qui con la sua cronologia di revisione.
