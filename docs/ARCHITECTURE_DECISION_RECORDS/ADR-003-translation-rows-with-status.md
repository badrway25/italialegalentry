# ADR-003 — Traduzioni come righe per lingua con stato di approvazione

**Stato:** accettata

## Decisione
Ogni modello traducibile ha una tabella `<Model>Translation(master, language, status, campi…)` derivata da `cms.TranslationBase`. Stati: `missing / draft / reviewed / approved / published`. Solo `published` è reso pubblico; altrimenti fallback alla lingua sorgente (FR) con attributo `lang`.

## Alternative scartate
- django-modeltranslation (colonne per lingua): nessuno stato per lingua, pubblicazione accidentale facile.
- django-parler: vicino, ma senza workflow di approvazione; dipendenza in più per poco valore.

## Conseguenze
Un contenuto non approvato non può finire online (gate G10). L'admin mostra la matrice lingua × stato (`cms.translation.translation_matrix`).
