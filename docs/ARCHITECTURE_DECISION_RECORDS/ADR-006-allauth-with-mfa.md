# ADR-006 — django-allauth (account + MFA) per l'autenticazione

**Stato:** accettata

## Decisione
`allauth.account` (login via e-mail, verifica obbligatoria, reset password, rate limit configurati) + `allauth.mfa` (TOTP + recovery codes) con adapter di progetto che **chiude la registrazione quando il gate G2 è chiuso**. Custom `accounts.User` (e-mail) definito dalla prima migrazione. Ruoli = gruppi `role:*`; policy object-level deny-by-default in `accounts.permissions`.

## Alternative
Auth views native + codice custom per verifica e-mail e MFA: più codice di sicurezza scritto in casa, maggiore rischio.

## Conseguenze
Template allauth ridisegnati nel design system (`templates/allauth/`).
