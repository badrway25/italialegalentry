# IMPLEMENTATION PHASES — Italy Legal Entry™ (rebuild Django)

Data di riferimento del progetto: **17 settembre 2026**. Lavoro esclusivamente locale (master prompt §2). Le fasi del Documento di Implementazione (14/09/2026) sono vincolanti per la priorità; le milestone M0–M12 (master prompt §98) organizzano il lavoro tecnico.

## 1. Fasi contrattuali (Documento di Implementazione) → milestone tecniche

| Fase documento | Scadenza | Contenuto (Impl.) | Milestone tecniche | Stato al 17/09 |
|---|---|---|---|---|
| **PHASE 1** | ≤ 17 settembre 2026 (oggi) | §1.1 Espace Entreprises (testi e form « Recueil des besoins »), §1.2 Espace Personnes (due sostituzioni), §1.3 marchio ™, §1.4 cinque pagine giuridiche autonome + gate sui form; e-mail unica contact@agamieuromed.org; versione nel footer | M0 → M1 → M2 → **M3** | M0 completata; M1–M3 in corso. Le pagine giuridiche restano `BLOCKED_BY_MISSING_OFFICIAL_SOURCE` (G1) e i form gated (G2): la scadenza è rispettabile per tutto ciò che dipende dal team; il testo IT dipende dal committente. |
| **PHASE 2** | ≤ 25 settembre 2026 | §2.1 pagina Forum Vénétie–Maroc (contenuto integrale, programma da back-office, iscrizione, bottoni secondari, transizione post-2/10), §2.2 banner home fino al 2/10 | **M4** (+ M1/M2 come prerequisito) | TODO — subito dopo M3 |
| **PHASE 3** | > 2 ottobre 2026 (salvo indicazione contraria) | §3.1 hero, §3.2 quattro accessi, §3.3 Espace Personnes e percorsi, §3.4 Institutions, §3.5 Universités, §3.6 Projet pilote, §3.7 alleggerimento grafico + RTL + versione, §3.8 contenuti addizionali (anti-frode, FAQ, glossario, Vivre en Italie, formazione dopo l'arrivo, Actualités/newsletter, Forum Virtuale), §3.9 diplomi, §3.10 CRM/espace réservé, §3.11 elementi da trasmettere | **M5 – M9** implementate ora, pubblicazione gated (G3, G11) | TODO — implementazione immediata dopo M4; pubblicazione ≥ 02/10 via flag |
| Trasversale | — | Sicurezza, accessibilità, performance, i18n/RTL, QA, red team, report | **M10 – M12** | TODO |

Regola: **non attendere il consenso del committente tra milestone**, salvo blocchi non risolvibili responsabilmente (testo legale ufficiale, loghi, credenziali, decisioni di pubblicazione/produzione, scelte giuridiche) — tracciati come `PENDING_CLIENT`/`BLOCKED_*`.

## 2. Milestone M0–M12: entry/exit criteria

| M | Nome | Entry criteria | Attività principali | Exit criteria (verificabili) | Fase doc. |
|---|---|---|---|---|---|
| **M0** | Discovery | avvio | Inventario ambiente/tool; lettura integrale PDF; ricerca Allegato 1 IT; audit sito live (10 viewport + AR/IT/FR, HTML/CSS/JS/headers, sitemap, app subdomain); git init; venv | estrazioni testuali complete (allora in `docs/source/`, dal 21/09 fuori dal repository); `docs/audit/current-site/` popolato; `REQUIREMENTS_MATRIX`, `CONTENT_SOURCE_MAP`, `LEGAL_AND_PUBLICATION_GATES`, `IMPLEMENTATION_PHASES` scritti; `CURRENT_SITE_AUDIT.md` redatto; ADR-000 (contesto) | 1 |
| **M1** | Architecture | M0 | ADR-001 Django 5.2 LTS; ADR-002 CMS custom vs Wagtail; ADR-003 no Celery v1; ADR-004 HTMX/vanilla; struttura app; settings split (base/dev/test/prod); PostgreSQL via Docker (porta 5439); custom `User`; `PublishableMixin`, `FeatureFlag`, `Translation`, `locked_content` registry + checksum; `core.gates`; audit; pytest config; ruff; `.env.example`; `docker-compose.yml`; README avvio | `manage.py check` ok; `migrate` ok su PostgreSQL; `makemigrations --check` pulito; `pytest` verde su test di fondazione (gates, flags, locked content); `docs/ARCHITECTURE.md` + ADR; commit "bootstrap architecture" | 1 |
| **M2** | Public Foundation | M1 | Design token (`tokens.css`), tipografia self-hosted, layout base (utility bar, header/mega-menu, drawer, breadcrumb, footer con 5 link legali distinti + anti-frode + versione), i18n_patterns 4 lingue, RTL logical properties, language switcher, skip link/landmarks, error pages, componenti base, sitemap/robots/SEO head, `HomepageBanner`, `HeroVariant`, `HomeSection` | Home e pagine placeholder renderizzate in 4 lingue senza overflow 320–1920; axe 0 serious su base; `docs/DESIGN_SYSTEM.md`; commit "design system" | 1 |
| **M3** | Phase 1 Compliance | M2 | Espace Entreprises (testi lockati) + `CompanyNeed` form 14 campi + consenso + CTA; sostituzioni Espace Personnes; wordmark ™; app `legal` con 5 route `BLOCKED`; G1/G2/G7/G8 attivi; e-mail centralizzata; footer versione; registro vietati + test compliance; nessun `MATCHING`/`®`/tagline vietata | `pytest tests/compliance` verde; form gated dimostrato (GET avviso / POST 403); review indipendente (Legal + Security) firmata in `QA_REPORT`; commit "phase 1 compliance" + "legal gating" | **1 (≤ 17/09)** |
| **M4** | Phase 2 Forum | M3 | App `forum` (10 modelli), pagina evento con sezioni nell'ordine del documento, programma seed + admin inline, `SpeakerRole` funzioni only (G5), slot loghi (G6), form iscrizione (7 campi + categoria 8 voci + settore + consenso), duplicati/rate limit/audit/CSV, bottoni secondari, `mode` evento/permanente (G4), sezioni permanenti, banner home schedulato | Pagina Forum 200 in 4 lingue, screenshot 360→1920 + AR; test forum verdi; freeze-time test banner; review indipendente; commit "forum phase 2" | **2 (≤ 25/09)** |
| **M5** | Ecosystem | M4 | Quattro accessi (max 4, `CheckConstraint`), Espace Personnes (8 percorsi seed, dettaglio con `CONTENT_PENDING_LEGAL_REVIEW`), Institutions + Universités (pagine + `CollaborationProposal`), Projet pilote + flow SVG 8 step, anti-frode (pagina, callout, footer); tutto `SCHEDULED 2026-10-02` (G3) | test `test_exactly_four_entrances`, `test_eight_pathways_order`, `test_sequence_eight_steps`, gate 404-before-date verdi; preview staff funzionante | 3 (gated) |
| **M6** | Orientation Platform | M5 | Rule engine (`RuleSet` versionato, `Question/Choice/Transition/Outcome`), wizard HTMX (progress, previous, explanation, keyboard), sessione anonima + save/resume autenticato (gated G2), `OrientationResult` con ruleset/disclaimer version, checklist, risultato "pré-évaluation à caractère informatif" | ruleset v1 `draft` seed; test branching/versioning; E2E tastiera; nessuna parola di promessa (F21) | 3 (gated) |
| **M7** | Content Ecosystem | M5 | FAQ (9 lockate + CMS), glossario (10 lockati + funzioni), Vivre en Italie (10 categorie), formazione prima/dopo, diplomi, news (workflow 4 stati) + newsletter (consenso separato, double opt-in dev), Forum Virtuale landing (G11) | test contenuti lockati; workflow news; newsletter non preselezionata/revocabile | 3 (gated) |
| **M8** | Reserved Area | M1 (auth) + M5 | `accounts` (email login, verifica, reset, throttling, TOTP staff), `Role`/`Membership`, `accounts/permissions.py` deny-by-default, `portal` dashboard per ruolo, `documents` privati, `notifications`; testi `p3.reserved.*` gated | test RBAC obbligatori (company A/B, person A/B, forum participant, staff limitato, IDOR documenti) verdi; review Security | 3 (gated) |
| **M9** | Future Infrastructure | M8 | `community` (rooms, discussions, posts, attachments, moderation, reports, calendar, initiatives, collaborations) dietro G11; `integrations` outbox/idempotency/external refs; `docs/CRM_INTEGRATION_CONTRACT.md` | test permessi community; test idempotency; flag off → 404 | 3 (gated) |
| **M10** | Hardening | M3–M9 | Security headers/CSP nonce, `check --deploy`, pip-audit, bandit, upload hardening, rate limit globale, logging strutturato + request id, performance (WebP/AVIF, lazy, budget JS/CSS), a11y pass completo, `docs/SECURITY.md`, `PRIVACY_BY_DESIGN.md`, `ACCESSIBILITY.md`, `DEPLOYMENT.md` | scan senza high; Lighthouse locale ≥ target (Perf ≥ 90, A11y ≥ 95, BP ≥ 95, SEO ≥ 95); axe 0 serious/critical su tutte le pagine × 4 lingue | X |
| **M11** | Full QA + Red Team | M10 | Browser E2E (Chromium + Firefox/WebKit se installabili), responsive 10 viewport, RTL LTR/RTL diff, visual golden, content/legal compliance, red team indipendente (agent non implementatori), correzioni, rerun completo | tutti i findings red team chiusi o dichiarati in `QA_REPORT`; suite completa verde; `docs/I18N_RTL.md`, `docs/QA_REPORT.md` | X |
| **M12** | Release Candidate LOCAL | M11 | Freeze; `makemigrations --check`; git status clean; README comandi esatti; report finale (18 punti) con stato LOCAL_RELEASE_READY / CONDITIONALLY_READY / NOT_READY | nessun deploy; tag `rc-local-1` | X |

## 3. Catena di review indipendente (master prompt §10)

**DEVELOPER → REVIEWER → QA → FINAL ACCEPTANCE.** L'agent che sviluppa non dichiara mai completata una feature critica. Ambiti obbligatori: legal, auth, permissions, GDPR, forms, multilingual, RTL, security, orientation, reserved area, uploads, Forum, CMS, production configuration.

| Ambito | Developer | Reviewer | QA | Final acceptance |
|---|---|---|---|---|
| Legal pages + gates G1/G2 | Legal Content Integration Specialist + Principal Django Engineer | GDPR/Privacy-by-design Specialist | QA Automation | Independent Final Reviewer |
| Auth / RBAC / portal | Authentication/RBAC Engineer, Reserved Area/Portal Engineer | Django Security Engineer | QA Automation + Security Testing | Independent Final Reviewer |
| Form pubblici (imprese, forum, collaborazioni, contatto, newsletter) | Principal Django Engineer / Forum Engineer | Django Security Engineer + GDPR Specialist | QA Automation | Technical Product Manager |
| i18n / RTL | RTL/i18n Specialist + Senior Frontend Engineer | Responsive/Mobile Specialist | QA (screenshot LTR/RTL) | Independent Final Reviewer |
| Orientation wizard + rule engine | Principal Django Engineer + Immigration Information UX Specialist | Legal Content Integration Specialist | QA Automation (E2E tastiera) | Technical Product Manager |
| Forum (P2) | Forum/Event Platform Engineer | Institutional Communication Specialist + Security Engineer | QA Automation | Principal Project Manager |
| CMS / back-office | CMS/Back-office Architect | Principal Software Architect | QA (admin smoke E2E) | Technical Product Manager |
| Upload / documents | Reserved Area/Portal Engineer | Django Security Engineer | Security Testing (IDOR, MIME) | Independent Final Reviewer |
| Production configuration | DevOps/Production Readiness Engineer | Django Security Engineer | QA (`check --deploy`) | Principal Software Architect |
| Design / UI | Senior Institutional UI Designer + Design System Specialist | Art Director + Accessibility Specialist | QA visual | Principal Project Manager |

Regola operativa: ogni PR/commit di feature critica riporta nel messaggio `Reviewed-by: <ruolo>`; la tabella dei review completati è mantenuta in `docs/QA_REPORT.md` §"Independent review".

## 4. Definition of Done

### 4.1 DoD — Design (master prompt §94)
Una pagina è completata solo se supera: gerarchia visiva; responsive (320/360/375/390/412/768/1024/1280/1440/1920, nessun overflow, tap target ≥ 24 px); tipografia (scala, misura di riga, wrapping AR/FR); spacing (token); interaction (hover/focus/active, motion con reduced-motion); accessibilità (axe 0 serious/critical, tastiera, focus visibile, contrasto AA); empty state; coerenza contenuti (solo testi lockati o marcati); performance (budget); RTL se applicabile (screenshot AR confrontati); screenshot review dell'Art Director.

### 4.2 DoD — Feature (master prompt §95)
1. Requisiti verificati (ID in `REQUIREMENTS_MATRIX`) · 2. Implementazione completa (service layer, thin view) · 3. Migrations corrette (`makemigrations --check`) · 4. Unit test · 5. Integration test · 6. Permission test (deny-by-default) · 7. Browser test se rilevante · 8. Accessibility test · 9. Responsive check · 10. Documentazione aggiornata · 11. Independent review (§3).

### 4.3 DoD — Contenuto
Testo lockato → via `{% locked %}`; testo di team → marcato (`ui`, `transitional`, `CONTENT_PENDING_LEGAL_REVIEW`), con `source_url`/`last_reviewed_at` dove giuridico; nessun marcatore visibile in pubblico; traduzioni solo `PUBLISHED`.

## 5. Team multi-agent: ruoli, ownership, app (master prompt §9)

Ownership esclusiva: un file appartiene a un solo owner per milestone; i file condivisi (`config/settings/*`, `config/urls.py`, `templates/base.html`, `static/css/tokens.css`, `cms/locked_content.py`) sono pre-cablati dall'orchestratore e modificati solo da lui o su suo mandato esplicito.

| # | Ruolo | Agent (nome operativo) | Ownership (app / directory / doc) | Milestone |
|---|---|---|---|---|
| 1 | Principal Project Manager / Orchestrator | `orchestrator` (sessione principale) | `docs/IMPLEMENTATION_PHASES.md`, `docs/QA_REPORT.md`, file condivisi, merge, commit | tutte |
| 2 | Principal Software Architect | `architect` | `docs/ARCHITECTURE.md`, `docs/ARCHITECTURE_DECISION_RECORDS/`, `config/`, `core/` (mixin, gates) | M1 |
| 3 | Technical Product Manager | `tpm` | `docs/REQUIREMENTS_MATRIX.md`, `docs/CONTENT_SOURCE_MAP.md`, accettazione | M0, M12 |
| 4 | Senior UX Architect | `ux-architect` | flussi (home, spazi, wizard), `docs/DESIGN_SYSTEM.md` §UX | M2, M5, M6 |
| 5 | Information Architecture Specialist | `ia` | tassonomia menu (`cms/fixtures/menu.json`), breadcrumb, `docs/URL_MIGRATION_MAP.md` | M2 |
| 6 | Senior Institutional UI Designer | `ui-designer` | `templates/components/`, `static/css/components/` | M2, M5 |
| 7 | Art Director | `art-director` | direzione immagini, `docs/IMAGE_LICENSES.md`, `static/img/` | M2, M5, M11 |
| 8 | Design System Specialist | `design-system` | `static/css/tokens.css`, `static/css/base.css`, `docs/DESIGN_SYSTEM.md` | M2 |
| 9 | Accessibility/WCAG Specialist | `a11y` | `tests/a11y/`, `docs/ACCESSIBILITY.md`, review componenti | M2, M10, M11 |
| 10 | Motion & Interaction Designer | `motion` | `static/js/motion.js`, transizioni CSS, reduced-motion | M2, M5 |
| 11 | Principal Django Engineer | `django-lead` | `pages/`, `ecosystem/`, `enquiries/`, `pathways/` | M3, M5 |
| 12 | Django Security Engineer | `security` | `config/settings/production.py`, `core/middleware.py`, `core/throttle.py`, `docs/SECURITY.md`, `tests/security/` | M3, M8, M10 |
| 13 | PostgreSQL/Data Architect | `data` | review modelli/constraints/indici, `docker-compose.yml` (db), migrazioni | M1, M4, M8 |
| 14 | Authentication/RBAC Engineer | `auth` | `accounts/` | M1 (User), M8 |
| 15 | API/Integration Architect | `integrations` | `integrations/`, `docs/CRM_INTEGRATION_CONTRACT.md` | M9 |
| 16 | Background Jobs/Notifications Engineer | `notifications` | `notifications/`, comandi `purge_expired_enquiries`, e-mail transazionali | M3, M8 |
| 17 | Senior Frontend Engineer | `frontend` | `templates/base.html` (su mandato), `static/js/`, HTMX | M2, M6 |
| 18 | Responsive/Mobile Specialist | `mobile` | `tests/e2e/test_responsive.py`, media query, drawer | M2, M11 |
| 19 | RTL/i18n Specialist | `i18n-rtl` | `locale/`, `cms/translation*`, `static/css/rtl.css` (se necessario), `docs/I18N_RTL.md`, `tests/e2e/test_rtl.py` | M2, M10, M11 |
| 20 | Web Performance Engineer | `perf` | WhiteNoise/compressione, immagini responsive, budget, Lighthouse | M10 |
| 21 | Legal Content Integration Specialist | `legal-content` | `legal/`, `cms/locked_content.py`, `cms/locked_content.sha256.json`, `cms/forbidden_content.py`, `tests/compliance/` | M3, M7 |
| 22 | GDPR/Privacy-by-design Specialist | `gdpr` | `consents/`, `docs/PRIVACY_BY_DESIGN.md`, retention, review form | M3, M7, M8 |
| 23 | Institutional Communication Specialist | `comms` | testi di team (UI, transitori), tono istituzionale, `partners/` | M2, M4 |
| 24 | Immigration Information UX Specialist | `immigration-ux` | struttura percorsi/checklist, `orientation/` (regole draft) | M5, M6 |
| 25 | CMS/Back-office Architect | `cms` | `cms/` (Publishable, FeatureFlag, HomeSection, Banner, Hero, Menu), `core/admin.py`, admin UX | M1, M3, M7 |
| 26 | Forum/Event Platform Engineer | `forum` | `forum/`, `community/` | M4, M9 |
| 27 | Reserved Area/Portal Engineer | `portal` | `portal/`, `documents/` | M8 |
| 28 | DevOps/Production Readiness Engineer | `devops` | `docker-compose.yml`, `Dockerfile`, `.env.example`, `docs/DEPLOYMENT.md`, `scripts/` | M1, M10 |
| 29 | QA Automation + Security Testing Specialist | `qa` | `tests/e2e/`, `tests/visual/`, `tests/security/`, `docs/QA_REPORT.md` (dati) | M3, M4, M11 |
| 30 | Independent Final Reviewer / Red Team | `red-team` (agent che non ha implementato) | findings in `docs/QA_REPORT.md` §Red team; nessuna ownership di codice | M11 |

Se l'ambiente supporta meno agent simultanei, i ruoli si combinano per competenza mantenendo la separazione developer/reviewer: (2+13), (4+5+24), (6+8+10), (7+23), (11+16), (12+28), (14+27), (15+26), (17+18+19+20), (21+22), (25+3), (9+29), 30 sempre distinto.

## 6. Piano di commit (master prompt §89)

`bootstrap architecture` → `design system` → `public foundation i18n` → `phase 1 compliance` → `legal gating` → `forum phase 2` → `ecosystem phase 3 (gated)` → `orientation platform` → `content ecosystem` → `reserved area` → `community + integrations` → `i18n RTL` → `hardening` → `QA + red team fixes` → `release candidate local`. Mai commitare `.env`, segreti, dump, cache, `node_modules`, `.venv`, file pesanti inutili.

## 7. Rischi e blocchi noti (17/09/2026)

| Rischio / blocco | Impatto | Mitigazione | Stato |
|---|---|---|---|
| Allegato 1 IT mancante | pagine legali vuote; form pubblici gated (G2) | struttura completa + comando di import; avviso "in preparazione"; nessun testo inventato | BLOCKED_BY_MISSING_OFFICIAL_SOURCE |
| app.legalitalentry.it non disponibile (503, certificato TLS errato per il nome) | nessun riferimento alla vecchia piattaforma; area riservata da ricostruire | `portal` foundation; nessun link esterno rotto | DONE (analisi) |
| Logo cliente con tagline "DIGITAL PATHWAYS TO ITALY" e porta (vietati in P3) | identità visiva | wordmark tipografico "Italy Legal Entry™" di default; logo caricabile da admin (`SiteIdentity.logo`) | LOGO_PENDING_CLIENT_CONFIRMATION |
| Traduzioni IT/EN/AR dei testi vincolati non trasmesse | pagine IT/EN/AR con fallback FR | G10, `lang="fr"`, cruscotto copertura | PENDING_CLIENT |
| Nomi intervenienti, loghi Regione/Comune, programma definitivo | pagina Forum parziale (come previsto dal documento) | G5, G6, programma editabile | PENDING_CLIENT |
| Hosting UE non attestato | nessun deploy | G12, `DEPLOYMENT.md` | PENDING_CLIENT |
| Testo di consenso per i form Contatto/Collaborazione non fornito | riuso del testo §1.1 con marcatura | `PENDING_CLIENT` per conferma | PENDING_CLIENT |
| Firefox/WebKit Playwright non installati | QA cross-browser limitata a Chromium | tentativo `playwright install firefox webkit`; documentare esito | TODO |
