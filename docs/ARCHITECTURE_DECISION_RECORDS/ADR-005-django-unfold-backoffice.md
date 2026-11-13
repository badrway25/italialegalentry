# ADR-005 — django-unfold per il back-office

**Stato:** accettata

## Contesto
Il brief chiede un back-office editoriale completo e usabile; il Django admin «grezzo» penalizza gli editor (navigazione, filtri, form lunghi).

## Decisione
django-unfold (0.107) sopra `django.contrib.admin`: tema, sidebar con ricerca, filtri avanzati, dashboard con stato dei gate (`core.admin_base.dashboard_callback`). Tutte le ModelAdmin ereditano da `core.admin_base.BaseModelAdmin`.

## Conseguenze
- UX editoriale moderna, nessun secondo CMS, nessuna risorsa esterna (asset serviti localmente).
- Dipendenza da un pacchetto terzo con release frequenti: versione pinnata, upgrade con QA.
