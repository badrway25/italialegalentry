# ADR-010 — Testi prescritti in un registro di codice con checksum

**Stato:** accettata

## Decisione
I testi «À INSÉRER — copier tel quel» vivono in `apps/cms/locked_content.py` (chiavi `p1.*`, `p2.*`, `p3.*`, `legal.*`), non in un database editabile. `scripts/verify_locked_against_source.py` dimostra che ogni frammento è sottostringa dell'estrazione del PDF; `locked_content.sha256.json` + test di conformità impediscono modifiche accidentali. Dove il documento richiede modificabilità dal back-office (programma Forum, FAQ, glossario) i record DB sono **seminati** dal registro e i campi bloccati sono read-only in admin (`LockedContentAdminMixin`).

## Conseguenze
Un cambio di testo è un commit revisionato, non un click. Le traduzioni ufficiali future si aggiungono come nuove tabelle di lingua nel registro.
