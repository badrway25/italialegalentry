# Convenzioni per gli agent (obbligatorie)

Questo documento è il contratto operativo per ogni agent specialistico. Leggerlo integralmente prima di
scrivere codice, insieme a `docs/ARCHITECTURE.md`, `docs/CONTENT_SOURCE_MAP.md`,
`docs/LEGAL_AND_PUBLICATION_GATES.md` e `docs/REQUIREMENTS_MATRIX.md`.

## 0. Regole non negoziabili
1. **Solo lavoro locale.** Mai toccare legalitalentry.it / app.legalitalentry.it, DNS, server, e-mail reali.
2. **Nessun testo giuridico inventato o tradotto.** Le 5 pagine legali restano `BLOCKED_BY_MISSING_OFFICIAL_SOURCE`.
   I testi prescritti si usano SOLO tramite `{% locked "chiave" %}` / `cms.locked_content.get()`. Mai copiarli
   a mano nei template, mai "migliorarli", mai tradurli con AI. Contenuto mancante → marcarlo
   `CONTENT_PENDING_LEGAL_REVIEW` nel codice/template (commento) e nel documento del proprio dominio.
3. **Formulazioni vietate**: vedi `apps/cms/forbidden.py` (MATCHING, Recruit in Morocco, ®, @legalitalentry.it, ecc.).
   Il marchio è sempre `Italy Legal Entry™`.
4. **E-mail pubblica unica**: `contact@agamieuromed.org` (via `settings.ILE` / `site.contact_email`). Mai `@legalitalentry.it`.
5. **Nessuna risorsa esterna** in runtime (font, immagini, script, iframe, analytics). CSP è `self`-only e
   il test di conformità fallisce con qualsiasi `https://` esterno nelle pagine.
6. **Nessun nome di personalità istituzionale**, nessun logo Regione/Comune inventato, nessuna promessa di visto/esito.
7. **Non usare git** (niente commit/branch/stash): l'orchestratore committa alle milestone.
8. **Ownership dei file**: modificare SOLO i file/directory assegnati nel proprio incarico. Se serve una modifica a
   file condivisi (`config/`, `templates/base.html`, `core/`, `cms/`), descriverla nel report finale invece di farla,
   salvo esplicita autorizzazione nell'incarico.

## 1. Ambiente
- Python: `.venv/Scripts/python` (Windows). Impostare `PYTHONIOENCODING=utf-8` per output Unicode.
- DB dev condiviso: `postgres://ile:ile-dev-password@127.0.0.1:5439/ile`.
- **Test DB dedicato per agent** (evita collisioni): esportare
  `TEST_DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_<nome_agent>` prima di `pytest`.
  Eseguire pytest con `-p no:cacheprovider --create-db` la prima volta.
- Dev server, se serve: porta dedicata (`runserver 127.0.0.1:87xx`), poi terminare il processo.
- Migrazioni: `manage.py makemigrations <propria_app>` e `manage.py migrate <propria_app>`; una sola migrazione
  iniziale pulita per app (rigenerarla, non accumularne).
- Lint prima di consegnare: `.venv/Scripts/python -m ruff check apps/<app> && ruff format apps/<app>`.

## 2. Codice
- Modelli: ereditare `core.models.TimeStampedModel` o `cms.models.PublishableModel`; traduzioni con
  `cms.models.TranslationBase` (FK `master`, `related_name="translations"`, `UniqueConstraint(master, language)`).
- Vincoli DB (`UniqueConstraint`, `CheckConstraint`), indici, `TextChoices`, validatori. Niente modelli-monolite.
- View sottili → logica in `services.py`. Nessuna logica di business nei template.
- Admin: ereditare `core.admin_base.BaseModelAdmin` / `BaseTabularInline` / `BaseStackedInline`;
  campi bloccati con `LockedContentAdminMixin.locked_fields`; `list_display`, `search_fields`, `list_filter`,
  `fieldsets`, `autocomplete_fields`, `date_hierarchy` dove sensato; export CSV come `actions`.
- Form pubblici: `core.forms.HoneypotFormMixin` + `PublicFormMixin` + `ConsentBooleanField` con label = testo
  bloccato; view con `core.throttle.allow(request, "<scope>")` (429 → `errors/429.html`), gate
  `core.gates.public_forms_enabled()` (se chiuso → template `components/form_unavailable.html`),
  consenso registrato con `consents.services.record_consent`, notifica `notifications.services.notify_forms_inbox`,
  audit `audit.services.record(request, action="…", target=obj)`. Spam (honeypot) → risposta di successo
  senza salvare. Dati minimi: solo i campi prescritti.
- Permessi object-level: registrare policy con `@accounts.permissions.policy(Model)`; nelle view usare
  `require(user, "view", obj)`. Default = negato.
- Date/gate: usare `core.clock.now()` (mai `timezone.now()` per decisioni di pubblicazione).
- Seeds idempotenti in `<app>/seeds.py` con `@core.seeds.register_seed("<app>.<nome>", order=N)`;
  mai sovrascrivere modifiche editoriali su campi non bloccati.
- Route pubbliche: registrarle in `AppConfig.ready()` con `core.public_routes.register_public_paths(...)`
  (con `requires_gate="phase3_public"` ecc. per le pagine gated). Sitemap: `core.sitemaps.register(name, Sitemap)`.
- URL names con namespace (`forum:detail`, `enquiries:company_needs`). Slug leggibili, stabili.
- Log: `logging.getLogger("ile.<app>")`; mai dati personali nei log.

## 3. Template e frontend
- Estendere `base.html`; blocchi: `page_title`, `meta_description`, `breadcrumbs`, `content`, `extra_head`,
  `extra_scripts`. Breadcrumb con `components/breadcrumbs.html` (fornito dal design system).
- Componenti disponibili in `templates/components/` (documentati in `docs/DESIGN_SYSTEM.md`): usare quelli
  esistenti prima di crearne di nuovi. Classi CSS BEM-like (`.block__element--modifier`), token via
  `var(--…)`, proprietà logiche (`margin-inline-start`, non `margin-left`), niente colori hard-coded.
- Icone: `{% svg_icon "nome" %}` (sprite `static/img/icons.svg`). Niente emoji, niente librerie icone miste.
- Immagini: solo `cms.MediaAsset` / file in `static/img/` con licenza registrata in `docs/IMAGE_LICENSES.md`.
- Accessibilità: landmark, gerarchia heading (un solo `h1`), label/`aria-describedby` sugli errori, focus visibile,
  contrasto AA, `prefers-reduced-motion`, tabelle con `th scope`, modali con focus trap.
- Stringhe UI: `{% translate %}` / `gettext_lazy` con sorgente in **francese** (le traduzioni IT/EN/AR arrivano
  dai `.po`). Testi prescritti: `{% locked %}`. Nessun testo hard-coded in inglese.
- Ogni pagina: `<title>` specifico, `meta description`, breadcrumb, stati vuoti/errore, RTL verificato.

## 4. Test (obbligatori per consegnare)
- `apps/<app>/tests/`: unit (modelli/servizi/regole), integration (view, form, permessi, gate), compliance
  (testi bloccati resi correttamente, nessuna formulazione vietata) — marker `compliance` / `security`.
- Fixture condivise in `tests/conftest.py` (`seeded`, `legal_published`, `phase3_open`, `before_phase3`,
  `set_flag`, `person_user`, `staff_user`, `superuser`, `user_factory`).
- Le pagine pubbliche devono passare `tests/compliance/test_public_pages.py` (registrando le route).
- Test di permessi: A non vede B (IDOR), anonimo → login, staff limitato → 403.

## 5. Consegna (report finale dell'agent)
Riportare: file creati/modificati, comandi eseguiti, output di `pytest` (conteggi), `ruff`, migrazioni,
route registrate, chiavi bloccate usate, gate applicati, cose lasciate `CONTENT_PENDING_LEGAL_REVIEW`,
richieste di modifica a file condivisi, rischi noti. Niente dichiarazioni di "completato" senza output di test.
