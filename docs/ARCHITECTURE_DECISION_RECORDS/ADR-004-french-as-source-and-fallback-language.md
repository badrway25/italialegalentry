# ADR-004 — Francese come lingua sorgente e di fallback

**Stato:** accettata (rivedibile)

## Contesto
Il documento di implementazione fornisce **solo** i testi francesi («la version française faisant foi entre-temps pour la version FR du site»); le versioni IT/AR/EN «seront transmises». Le pagine legali esistono solo in italiano ufficiale (assente).

## Decisione
`LANGUAGE_CODE = "fr"`, `CONTENT_FALLBACK_LANGUAGE = "fr"`. URL con prefisso per tutte le lingue (`/fr/`, `/it/`, `/en/`, `/ar/`); la radice reindirizza secondo `Accept-Language`. Le stringhe UI (menu, pulsanti generici, messaggi di validazione) hanno sorgente FR e traduzioni IT/EN/AR via gettext. I testi bloccati sono resi in FR anche nelle altre lingue, marcati `lang="fr"`, finché non arrivano versioni ufficiali.

## Conseguenze
Cambiare lingua predefinita in IT quando arriveranno i testi ufficiali è una modifica di configurazione (una riga) + file `.po`.
