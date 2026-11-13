# ADR-002 — CMS custom su Django admin invece di Wagtail

**Stato:** accettata

## Contesto
Wagtail 8 offre page tree, StreamField, revisioni, scheduling e localizzazione (wagtail-localize). Il dominio ILE però è fatto di **testi prescritti e bloccati**, gate di pubblicazione temporali, stati di traduzione con approvazione, modelli evento/forum/iscrizioni/consensi/percorsi e un'area riservata con RBAC.

## Decisione
CMS custom: `cms.PublishableModel` (workflow + scheduling + versione), `cms.TranslationBase` (stato per lingua), registro testi bloccati in codice con checksum, back-office `django.contrib.admin` + django-unfold. Nessun page tree generico.

## Motivazioni
- I contenuti del documento non sono "pagine libere": sono strutture (programma, FAQ, glossario, percorsi) che gli editor modificano senza poter alterare i testi bloccati → modelli espliciti battono StreamField.
- Un unico sistema di permessi (RBAC + policy object-level) per sito e area riservata; Wagtail introdurrebbe un secondo modello di autorizzazioni e una seconda admin.
- Dipendenza pesante (Wagtail + wagtail-localize + editor JS) non giustificata dai requisiti.

## Conseguenze
- Modello dati pulito, testabile, gate reali.
- Preview e diff di revisione vanno implementati in modo mirato: versione + `published_at` + snapshot immutabili per contenuti sensibili (legal).
