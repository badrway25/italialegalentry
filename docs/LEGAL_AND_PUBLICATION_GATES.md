# LEGAL AND PUBLICATION GATES — Italy Legal Entry™

Data di riferimento: 17 settembre 2026. Questo documento definisce i **gate di pubblicazione** come meccanismi software reali (modelli, flag, funzioni, test), non come note. Un gate chiuso impedisce la pubblicazione o l'attivazione della funzione a livello server: nessun template, nessun editor e nessun errore di configurazione può aggirarlo senza lasciare traccia nell'audit.

## 0. Principi e infrastruttura comune

| Elemento | Implementazione |
|---|---|
| Registro testi vincolati | `cms/locked_content.py` — `LOCKED: Mapping[str, str \| list]` + `LOCK_CLASS: Mapping[str, LockClass]` (`LOCKED_IMPLEMENTATION_CONTENT`, `LOCKED_LEGAL_CONTENT`). Import-only; nessun accesso ORM. |
| Checksum | `cms/locked_content.sha256.json` — `{key: sha256(normalized_text)}`. Comando `manage.py lock_content --verify` (usato dal test) e `--update --reason "<riferimento trasmissione scritta>"` (scrive `docs/CONTENT_LOCK_CHANGELOG.md`). |
| Feature flag | `cms.FeatureFlag(key unique, enabled bool, enabled_from datetime null, enabled_until datetime null, note, updated_by, updated_at)`; API `cms.flags.is_enabled(key, now=None)`; ogni modifica genera `audit.AuditEvent(action="flag.change")`. Seed dei flag in `cms/fixtures/feature_flags.json` (tutti `enabled=False` salvo indicato). |
| Publishable | `cms.PublishableMixin`: `status ∈ {DRAFT, REVIEW, SCHEDULED, PUBLISHED, ARCHIVED, BLOCKED}`, `publish_from`, `publish_until`, `published_at`, `last_reviewed_at`, `version`, `author`, `editor`, `reviewer`. Manager `.public(now)` = `status=PUBLISHED AND (publish_from IS NULL OR ≤ now) AND (publish_until IS NULL OR > now)`. Le view pubbliche usano SOLO `.public()`. |
| Gate evaluator | `core/gates.py`: funzioni pure `legal_pages_published()`, `forms_enabled()`, `phase3_public()`, `virtual_forum_enabled()`, `speaker_names_visible(event)`, `partner_logo_visible(partner)`, `translation_renderable(key, lang)`; context processor `core.context_processors.gates` espone lo stato ai template; pannello admin `/admin/gates/` (read-only) mostra ogni gate con stato, motivo, ultima modifica. |
| Audit | `audit.AuditEvent(actor, action, target_type, target_id, before/after JSON, reason, ip_hash, created_at)`; immutabile (nessun `update/delete` via admin). |
| Test | `tests/compliance/test_publication_gates.py` (uno o più test per gate) + test specifici citati sotto. |
| Override amministrativo | Consentito solo dove indicato, sempre tramite `FeatureFlag` dedicato con `note` obbligatoria (≥ 20 caratteri, riferimento alla comunicazione scritta) e `AuditEvent`. Nessun override via variabile d'ambiente in produzione. |

---

## G0 — Integrità dei testi vincolati (content lock)

| Voce | Dettaglio |
|---|---|
| Trigger | Qualunque differenza tra il testo nel registro e il checksum archiviato; qualunque rendering pubblico di una chiave vincolata con testo diverso dal registro. |
| Meccanismo | Registro immutabile in codice; templatetag `{% locked "p1.companies.title" %}` (unica via per stampare un testo vincolato); `lock_content --verify` confronta SHA-256; il test renderizza ogni pagina in cui la chiave è collocata e verifica la presenza del testo esatto. |
| Visibilità admin | Pagina `/admin/gates/` sezione "Content lock": esito ultima verifica, data, chiavi. Le FAQ e i termini di glossario lockati mostrano in admin campo `locked=True` e i campi testo in sola lettura. |
| Test | `compliance/test_locked_content.py::test_checksums`, `::test_every_key_rendered_where_placed`, `faq/test_faq.py::test_locked_answers_not_editable`, `glossary/test_glossary.py::test_locked_terms_not_editable` |
| Sblocco | Solo su nuova trasmissione scritta dell'Avv. Badrane: aggiornare il registro, eseguire `lock_content --update --reason "<data e riferimento>"`, commit dedicato "content: update locked text <chiave> per trasmissione del <data>". |
| Owner | Legal Content Integration Specialist (modifica) → Independent Final Reviewer (verifica) |

## G1 — Pagine giuridiche: testo ufficiale italiano mancante

| Voce | Dettaglio |
|---|---|
| Trigger | L'"Allegato 1 — Testi legali" (versione italiana ufficiale) non è disponibile (verificato il 17/09/2026: assente in `C:\tmp`). Il Documento di Implementazione vieta di redigere o tradurre i testi giuridici (p.1; p.3 §1.4). |
| Meccanismo | `legal.LegalDocument(kind ∈ {PRIVACY, COOKIES, NOTICES, TERMS, DISCLAIMER}, language, body, is_official, status, source_reference, effective_from, last_revised_at, version)`. Seed: 5 documenti `language="it"`, `is_official=True`, `body=""`, `status=BLOCKED`, `source_reference="Allegato 1 — Testi legali (non ricevuto)"`. Le 5 route esistono e sono distinte (`/it/privacy-policy/`, `/it/cookie-policy/`, `/it/note-legali/`, `/it/condizioni-di-utilizzo/`, `/it/avvertenze/` + equivalenti sotto `/fr/ /en/ /ar/` che rinviano al documento IT). Con `status=BLOCKED` la view rende il template `legal/blocked.html`: titolo della pagina, avviso "Testo ufficiale in corso di pubblicazione" (IT + lingua corrente), titolare AGAMI e contatto `contact@agamieuromed.org`, `<meta name="robots" content="noindex">`. **Nessun testo giuridico generato, tradotto o "provvisorio" viene mai renderizzato.** Il testo FR di cortesia (Annexe 1) è archiviato nel registro come `legal.<kind>.fr_courtesy` e può essere pubblicato **solo** creando un `LegalDocument(language="fr", is_official=False, courtesy_notice=True)` con `status=PUBLISHED` dopo `FeatureFlag legal_fr_courtesy_authorized` (note = riferimento alla conferma scritta). Il template FR di cortesia stampa obbligatoriamente « Traduction de courtoisie — la version italienne fait foi » e un link alla pagina IT. La "Note opérationnelle pour le développeur (à ne pas publier)" della Cookie Policy non è nel registro pubblicabile (vedi G9). |
| Visibilità admin | Elenco `LegalDocument` con colonna `status` colorata; banner in cima all'admin: "5 pagine legali BLOCKED — i form pubblici sono disattivati (G2)". Pannello `/admin/gates/` → G1: RED. |
| Test | `legal/test_legal_gate.py::test_five_distinct_routes`, `::test_blocked_notice_no_fake_text` (nessuna parola dell'Annexe FR nella pagina IT bloccata; nessun testo > 400 caratteri nel body), `::test_fr_en_ar_point_to_italian`, `::test_cookie_internal_note_never_rendered` (stringa "Note opérationnelle" assente da ogni pagina e da ogni fixture pubblica), `::test_courtesy_fr_requires_flag`, `::test_footer_links_resolve` |
| Sblocco | 1) Ricezione dell'Allegato 1 IT; 2) import integrale via `manage.py import_legal_document --kind privacy --file <path> --version 1.0` (nessuna riformulazione; il comando registra SHA-256 del file sorgente in `source_reference`); 3) esclusione della nota interna della Cookie Policy (il comando rifiuta un file che contenga "Nota operativa" / "Note opérationnelle" e chiede `--strip-internal-note`); 4) review da parte di Legal Content Integration Specialist (`status=REVIEW`); 5) pubblicazione da admin (`status=PUBLISHED`, `effective_from`); 6) automaticamente G2 si riapre; 7) aggiornare `SiteIdentity.content_version`. |
| Owner | Legal Content Integration Specialist; approvazione: Avv. Badrane (esterna) |

## G2 — Form pubblici condizionati alle pagine legali

| Voce | Dettaglio |
|---|---|
| Trigger | Documento di Implementazione p.3 §1.4: "La publication de ces pages conditionne le maintien en activité des formulaires : si elles ne peuvent pas être mises en ligne immédiatement, désactiver les formulaires dans l’intervalle." |
| Meccanismo | `core.gates.forms_enabled()` = `legal_pages_published()` (tutti e 5 i `LegalDocument` IT `is_official=True` con `status=PUBLISHED`) **oppure** `FeatureFlag forms_override_enabled` con note obbligatoria (solo per test/staging: in produzione il flag è ignorato se `settings.ENV == "production"`). Form soggetti (tutti quelli che raccolgono dati personali): `CompanyNeedsForm` (Recueil des besoins), `ForumRegistrationForm`, `CollaborationProposalForm` (istituzioni/università), `ContactForm`, `NewsletterForm`, `RegistrationForm` (creazione account), `OrientationSaveForm` (salvataggio wizard su account). Le view ereditano `core.views.GatedFormView`: se il gate è chiuso, `GET` rende `components/form_unavailable.html` (messaggio: "Ce formulaire sera disponible dès la publication des informations sur le traitement des données personnelles" + contatto e-mail), `POST` restituisce HTTP 403 con lo stesso messaggio e **non** persiste nulla, né invia e-mail. Il wizard di orientamento resta utilizzabile in modalità anonima (nessun dato personale) ma il salvataggio è gated. |
| Visibilità admin | Pannello `/admin/gates/` → G2: stato + elenco form disattivati; badge "Form disattivati (G2)" nella pagina di lista di `CompanyNeed`, `ForumRegistration`, `CollaborationProposal`. |
| Test | `compliance/test_publication_gates.py::test_forms_disabled_while_legal_blocked` (per ogni form: GET mostra avviso e nessun `<form method="post">` con campi dati; POST → 403 e `Model.objects.count()==0` e `mail.outbox==[]`), `::test_forms_enabled_when_legal_published`, `::test_override_flag_ignored_in_production`, `::test_override_requires_note_and_audit` |
| Sblocco | Automatico alla chiusura di G1 (nessuna azione manuale). Override temporaneo (non produzione): `FeatureFlag forms_override_enabled` con note. |
| Owner | Django Security Engineer (meccanismo) → GDPR/Privacy-by-design Specialist (review) |

## G3 — Phase 3: date gate e feature flag

| Voce | Dettaglio |
|---|---|
| Trigger | Documento di Implementazione p.7: "PHASE 3 — Après le 2 octobre 2026 (sauf indication contraire)"; master prompt §6/§31: implementare ora, non pubblicare prima. |
| Meccanismo | `FeatureFlag phase3_public` (`enabled=False`, `enabled_from=2026-10-02T00:00 Europe/Rome`). `core.gates.phase3_public(now)` = `flag.enabled AND (enabled_from IS NULL OR enabled_from ≤ now)`. **Regola di sicurezza**: anche con `enabled=True`, il gate resta chiuso prima del 2 ottobre 2026 salvo `FeatureFlag phase3_early_authorized` con note (riferimento a "indication contraire" scritta). Contenuti gated: `HeroVariant(phase=3)`, `EcosystemEntrance` (testi `p3.entrances.*`), Espace Personnes (`p3.persons.*`), Espace Institutions, Espace Universités, Projet Pilote, Attention aux fraudes, FAQ, Glossaire, Vivre en Italie, Formation après l’arrivée, Actualités + newsletter, Diplômes, Espace réservé (testi), Forum Virtuel (anche G11). Ogni oggetto gated ha `status=SCHEDULED, publish_from=2026-10-02`; il manager `.public()` li esclude automaticamente prima della data; il template della home sceglie la variante hero via `phase3_public()`. Le route delle pagine P3 esistono sempre: prima del gate rispondono **404** al pubblico (non "coming soon", per evitare indicizzazione) e sono visibili allo staff con `?preview=<token firmato>` (`cms.preview`). Le URL non compaiono in sitemap/menu finché gated. |
| Visibilità admin | `/admin/gates/` → G3: countdown alla data, elenco oggetti `SCHEDULED`; azione "Anteprima Phase 3" genera link firmato valido 1 h. |
| Test | `compliance/test_phase3_gate.py::test_hero_p3_after_gate` (freeze time 2026-10-01 23:59 → hero transitorio; 2026-10-02 00:00 + flag → hero P3), `::test_p3_pages_404_before_gate`, `::test_p3_pages_not_in_sitemap_or_menu_before_gate`, `::test_staff_preview_token`, `::test_early_flag_requires_authorization`, `cms/test_feature_flags.py` |
| Sblocco | Il 2 ottobre (o dopo): admin imposta `phase3_public.enabled=True` (una sola azione, nessun deploy). Facoltativo: transizione automatica se `enabled=True` è già impostato con `enabled_from` = 2/10. |
| Owner | CMS/Back-office Architect → Technical Product Manager (accettazione) |

## G4 — Forum: modalità evento / permanente e banner home

| Voce | Dettaglio |
|---|---|
| Trigger | Impl. p.6 §2.1 Note ("après le 2 octobre, la page devient celle du FORUM PERMANENT VÉNÉTIE–MAROC") e §2.2 (banner "jusqu’au 2 octobre"). |
| Meccanismo | `ForumEvent.mode ∈ {UPCOMING, LIVE, PERMANENT}` + `permanent_from` (default `2026-10-03T00:00 Europe/Rome`) + `permanent_title` (default "FORUM PERMANENT VÉNÉTIE–MAROC"). `ForumEvent.effective_mode(now)` = `PERMANENT` se `mode==PERMANENT` o `now ≥ permanent_from`; altrimenti `mode`. Il template `forum/event_page.html` rende: in UPCOMING/LIVE → header evento, programma, INTERVIENNENT, INSCRIPTION (form gated G2), bottoni secondari; in PERMANENT → header permanente, sezioni "Interventions" (`ForumTalk`), "Photos/Vidéos" (`ForumMedia`), "Documents" (`ForumDocument`), "Accords et conventions" (`ForumAgreement`), "Partenaires" (`ForumPartner`), "Résultats" (`ForumOutcome`), "Prochains rendez-vous" (`ForumNextEvent`), Forum Virtuel (G11); il form di iscrizione all'evento passato è chiuso (`registration_open=False` automatico). Banner home: `cms.HomepageBanner(publish_from=now, publish_until=2026-10-02T23:59:59 Europe/Rome)` → scompare automaticamente; l'admin può anticipare/prolungare (audit). |
| Visibilità admin | `ForumEvent` change form: campo `mode` con help "Passa a PERMANENT dopo il 2/10 (automatico da `permanent_from`)"; `HomepageBanner` list con colonna "visibile ora". |
| Test | `forum/test_forum_mode.py::test_switch_to_permanent` (manuale e automatico per data), `::test_registration_closed_in_permanent`, `::test_permanent_sections_render_only_published_items`, `cms/test_home_banner.py::test_banner_until_2_october` (freeze 2026-10-02 23:00 → visibile; 2026-10-03 00:01 → assente) |
| Sblocco | Nessuno necessario (automatico); modifica manuale da admin sempre possibile. |
| Owner | Forum/Event Platform Engineer → QA |

## G5 — Nomi degli intervenienti istituzionali

| Voce | Dettaglio |
|---|---|
| Trigger | Impl. p.5 §2.1 Note: "aucun nom de personnalité institutionnelle ne doit être publié : seules les fonctions apparaissent. Les noms seront ajoutés avec le programme définitif, sur transmission écrite de l’Avv. Badrane." |
| Meccanismo | `forum.SpeakerRole(event, order, function_label, person_name blank, organisation blank, names_authorized=False, authorization_reference blank, authorized_by, authorized_at)`. `clean()`: `names_authorized=True` richiede `authorization_reference` (≥ 10 caratteri). Template: `{% if speaker.names_authorized and gates.speaker_names_visible %}{{ speaker.person_name }}{% endif %}` — di default stampa solo `function_label`. Gate globale `FeatureFlag forum_speaker_names_authorized` (deve essere `True` **e** il singolo record deve essere autorizzato). Test di contenuto: nessuna sequenza "Nome Cognome" (pattern maiuscole) nella sezione INTERVIENNENT quando il gate è chiuso; il seed contiene solo le 4 funzioni del documento. |
| Visibilità admin | Inline `SpeakerRole` in `ForumEvent` con colonna "Nome pubblicato?" (icona). Pannello gate G5. |
| Test | `forum/test_forum_page.py::test_speakers_functions_only`, `::test_no_person_names_public`, `forum/test_models.py::test_speaker_authorization_requires_reference` |
| Sblocco | Ricezione scritta del programma definitivo con i nomi → admin: compila `person_name`, `names_authorized=True`, `authorization_reference="e-mail Avv. Badrane del <data>"`; attiva `forum_speaker_names_authorized`. Audit automatico. |
| Owner | Forum/Event Platform Engineer → Institutional Communication Specialist (review) |

## G6 — Loghi ufficiali (Regione del Veneto, Comune di Rovigo, partner)

| Voce | Dettaglio |
|---|---|
| Trigger | Impl. p.4 §2.1 Note: "les logos de la Région et de la Commune seront transmis séparément avec leurs autorisations : prévoir leur emplacement dès maintenant"; master prompt §27: non inventarli, non scaricarli, placeholder solo in back-office/dev. |
| Meccanismo | `partners.Partner(name, kind ∈ {PATRONAGE, INSTITUTIONAL, ECONOMIC, ACADEMIC, OTHER}, logo (upload privato), website, authorized=False, authorization_reference, authorized_at)` + `forum.ForumPartner(event, partner, role, order)`. Template: lo slot patrocinio mostra il logo **solo se** `partner.authorized and partner.logo`; altrimenti mostra il solo nome testuale ("Région de la Vénétie", "Commune de Rovigo") come da testo vincolato `p2.forum.header.patronage` — mai un'immagine segnaposto. In `DEBUG=True` e per utenti staff il template mostra un riquadro tratteggiato "Emplacement logo — en attente d'autorisation" (classe `.dev-placeholder`, non renderizzata in produzione). Seed: 2 `Partner` PATRONAGE con `authorized=False`, `logo=None`. Test statico: `static/img/` non contiene file con nomi `*veneto*`, `*rovigo*`, `*regione*`, `*comune*`. |
| Visibilità admin | Lista `Partner` con colonna `authorized`; avviso nel change form: "Caricare solo loghi trasmessi con autorizzazione scritta". |
| Test | `forum/test_forum_page.py::test_patronage_no_fake_logos` (nessun `<img>` nello slot patrocinio; nome testuale presente), `partners/test_partner_gate.py::test_logo_hidden_until_authorized`, `compliance/test_images.py::test_no_unauthorized_institutional_logo_files` |
| Sblocco | Ricezione loghi + autorizzazioni → upload in admin, `authorized=True`, `authorization_reference`; registrazione in `docs/IMAGE_LICENSES.md` (fonte "fornito dal committente con autorizzazione del <data>"). |
| Owner | Institutional Communication Specialist → Art Director (resa) |

## G7 — Marchio: ™ obbligatorio, ® vietato

| Voce | Dettaglio |
|---|---|
| Trigger | Impl. p.3 §1.3: "Italy Legal Entry™"; "le symbole ® ne sera introduit que sur communication expresse de l’Avv. Badrane, après enregistrement de la marque"; mai "Marchio registrato / Registered trademark / Marque enregistrée". |
| Meccanismo | Templatetag `{% brand %}` → `Italy Legal Entry™` (unica sorgente del wordmark testuale; `<span class="tm" aria-hidden="true">™</span>` con testo accessibile "marque déposée"/"marchio depositato" secondo lingua). `FeatureFlag trademark_registered_symbol` (`enabled=False`): quando (e solo quando) attivato con note, `{% brand %}` usa ®. Registro vietato F08–F11 verificato su HTML pubblico di ogni pagina/lingua, template, `.po`, `static/` (SVG inclusi), seed e e-mail. |
| Visibilità admin | `/admin/gates/` → G7: "™ attivo — ® non autorizzato". |
| Test | `compliance/test_trademark.py::test_tm_symbol_present_no_registered` (ogni pagina pubblica contiene "Italy Legal Entry™" e non contiene `®`/`&reg;`/`&#174;`/`&#xAE;`), `::test_no_registered_wording`, `::test_words_fr`, `::test_words_it_no_registrato`, `::test_registered_flag_switch` |
| Sblocco | Comunicazione espressa dell'Avv. Badrane dopo la registrazione → `trademark_registered_symbol.enabled=True` con note; aggiornare il test (`®` ammesso) nello stesso commit; aggiornare `SiteIdentity.content_version`. |
| Owner | Legal Content Integration Specialist |

## G8 — Indirizzi e-mail pubblici

| Voce | Dettaglio |
|---|---|
| Trigger | Impl. p.2 §1.1 Note: tutti i form → `contact@agamieuromed.org`; nessun indirizzo `@legalitalentry.it` finché le caselle non sono attivate (p.15 §3.11). |
| Meccanismo | `settings.PUBLIC_CONTACT_EMAIL = "contact@agamieuromed.org"` e `settings.FORMS_RECIPIENT_EMAIL` (da `.env`, default identico); `core.checks` (Django system check, tag `ile.email`) fallisce all'avvio se uno dei due contiene `legalitalentry.it` e `FeatureFlag legalitalentry_mailboxes_active` non è attivo. Templatetag `{% contact_email %}` unica via per stampare l'indirizzo. `DEFAULT_FROM_EMAIL` in dev = `noreply@localhost`; in produzione da configurare con dominio attivo autorizzato (documentato in `DEPLOYMENT.md`). Registro F16 (regex `@legalitalentry\.it`) verificato su HTML pubblico, template, `.po`, seed, `static/`, e-mail generate nei test. |
| Visibilità admin | `/admin/gates/` → G8: indirizzo pubblico corrente, destinatario form, stato flag caselle. |
| Test | `compliance/test_public_email.py::test_only_agami_address_public`, `::test_no_legalitalentry_addresses`, `::test_forms_recipient`, `core/test_checks.py::test_email_check_fails_on_legalitalentry_domain` |
| Sblocco | Comunicazione di attivazione delle caselle → `.env` aggiornato + `legalitalentry_mailboxes_active.enabled=True` con note; aggiornare Privacy Policy (Annexe §1.1 lo prevede) tramite nuova versione ufficiale (G1). |
| Owner | DevOps/Production Readiness Engineer → GDPR Specialist |

## G9 — Analytics e tracking

| Voce | Dettaglio |
|---|---|
| Trigger | Annexe 1 §2 (solo cookie tecnici) + nota operativa interna (non pubblicabile): "ce texte n’est valable que tant qu’aucun outil d’analyse ou de traçage n’est installé sur le site (Google Analytics, pixels, cartes interactives avec cookies, vidéos intégrées). Avant d’installer tout outil de ce type, avertir la soussignée : cela exige un bandeau de consentement et la révision de l’information." Master prompt §54. |
| Meccanismo | Nessuna dipendenza/script di analytics. `core/analytics.py`: interfaccia `track(event, props)` con backend `NullAnalytics` (unico disponibile); l'eventuale backend futuro dovrà dichiarare `requires_consent=True` e non potrà essere attivato senza `FeatureFlag analytics_enabled` + `ConsentBanner` (non implementato: PROPOSTA FUTURA in `docs/SECURITY.md`). CSP in produzione: `default-src 'self'; script-src 'self' 'nonce-…'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-src 'none'` → qualunque tracker viene bloccato dal browser anche se introdotto per errore. Registro F23/F24 verificato su HTML e template. Cookie ammessi: `sessionid`, `csrftoken`, `django_language` (+ `messages` transiente). |
| Visibilità admin | `/admin/gates/` → G9: "Nessun analytics attivo — Cookie Policy valida"; elenco cookie emessi (dal test). |
| Test | `compliance/test_no_tracking.py::test_no_analytics_scripts`, `::test_no_external_font_or_image_hosts`, `::test_only_technical_cookies` (Set-Cookie nelle risposte pubbliche ⊆ set ammesso), `security/test_headers.py::test_csp_blocks_third_parties` |
| Sblocco | Decisione del committente + revisione Cookie Policy (nuova versione ufficiale, G1) + banner di consenso conforme alle Linee guida del Garante 10/06/2021 → solo allora `analytics_enabled`. |
| Owner | GDPR/Privacy-by-design Specialist → Django Security Engineer |

## G10 — Traduzioni: stato e fallback

| Voce | Dettaglio |
|---|---|
| Trigger | Impl. p.1: "les textes correspondants des autres versions linguistiques seront transmis par la soussignée"; p.15 §3.11: versione francese fa fede nel frattempo; master prompt §53: nessuna traduzione AI di contenuti legali/vincolati; stati missing → published. |
| Meccanismo | `cms.Translation(key, language ∈ {it, fr, en, ar}, text, status ∈ {MISSING, DRAFT, REVIEWED, APPROVED, PUBLISHED}, source ∈ {OFFICIAL, TEAM_UI, COURTESY}, reviewer, approved_at)`; `UniqueConstraint(key, language)`. Per le chiavi vincolate (`p1.*`, `p2.*`, `p3.*`) la lingua `fr` è servita dal registro lockato (non da DB) e le altre lingue solo se `Translation.status=PUBLISHED AND source=OFFICIAL`. `core.gates.translation_renderable(key, lang)` → il templatetag `{% locked key %}` rende il testo nella lingua richiesta se renderable, altrimenti il FR con `<span lang="fr">…</span>` (o `lang="fr"` sull'elemento contenitore) e classe `.fallback-lang` (nessun avviso invadente; attributo `data-translation-status`). Le stringhe UI (`.po`) restano traducibili dal team (marcate `source=TEAM_UI`). Le pagine legali seguono G1 (IT ufficiale unica). `manage.py translation_report` elenca chiavi `MISSING` per lingua. |
| Visibilità admin | Lista `Translation` filtrabile per stato/lingua; cruscotto "Copertura traduzioni" (% per lingua); pubblicazione richiede `reviewer` ≠ `author`. |
| Test | `compliance/test_translation_gate.py::test_unapproved_never_rendered` (Translation IT `DRAFT` per `p1.companies.title` → pagina IT mostra FR con `lang="fr"`), `::test_fr_fallback_lang_attr`, `::test_published_official_rendered`, `::test_legal_keys_not_translatable_via_cms` |
| Sblocco | Ricezione testi IT/AR/EN → inserimento come `source=OFFICIAL`, `status=REVIEWED` → review → `PUBLISHED`. |
| Owner | RTL/i18n Specialist (meccanismo) → Legal Content Integration Specialist (contenuti) |

## G11 — Forum Virtuale

| Voce | Dettaglio |
|---|---|
| Trigger | Impl. p.12 §3.8.7 Note: architettura prevista da subito; lancio dopo il Forum in Marocco (29/10 Casablanca, 30/10 Rabat); accesso riservato, moderato, dati non visibili senza consenso; master prompt §51. |
| Meccanismo | `FeatureFlag virtual_forum` (`enabled=False`, `enabled_from=null`). Con flag off: nessun link nel menu/pagina Forum, route `/…/forum-virtuel/` → 404 pubblico (staff: preview); il testo `p3.virtual_forum.*` è comunque gated anche da G3. Con flag on: landing con testo vincolato e CTA → login; accesso alle stanze solo a `User` con `Membership.role ∈ {institution, company, university, professional, moderator, staff}` e `ParticipantProfile.terms_accepted_version` + `privacy_accepted_version` valorizzati (richiede G1 aperto). `ParticipantProfile.visibility` default `PRIVATE`; `Post` visibile solo ai membri della `Room`; allegati su storage privato con download autorizzato. |
| Visibilità admin | `/admin/gates/` → G11; moduli `community` in admin con badge "Feature disattivata". |
| Test | `community/test_virtual_forum_gate.py::test_hidden_when_flag_off`, `::test_text_when_flag_on`, `::test_requires_terms_and_privacy_acceptance`, `community/test_permissions.py::test_non_member_cannot_read_room`, `::test_profile_private_by_default` |
| Sblocco | Dopo il 30/10/2026 e su decisione del committente: `virtual_forum.enabled=True`; richiede G1 aperto (Conditions + Privacy pubblicate): il flag rifiuta l'attivazione (`clean()`) se G1 è chiuso. |
| Owner | Forum/Event Platform Engineer + Authentication/RBAC Engineer → Django Security Engineer (review) |

## G12 — Hosting UE e attestazione di localizzazione

| Voce | Dettaglio |
|---|---|
| Trigger | Impl. p.3 §1.4: "Confirmer par écrit que l’hébergement du site et de la plateforme et les données collectées résident sur des serveurs situés dans l’Union européenne, avec indication du prestataire et de la localisation." Annexe §1.6. |
| Meccanismo | Documentale + configurazione: `docs/DEPLOYMENT.md` §"EU hosting attestation" con tabella (componente, prestatore, regione, riferimento contrattuale/DPA ex art. 28) da compilare **prima** del deploy; `settings/production.py` rifiuta l'avvio se `HOSTING_REGION` non è in `EU_REGIONS` (system check `ile.hosting`). Nessun servizio esterno extra-UE è referenziato dal codice (font/immagini self-hosted, e-mail via SMTP del prestatore UE da configurare, nessun CDN). |
| Visibilità admin | `/admin/gates/` → G12: valore di `HOSTING_REGION` e stato attestazione (`PENDING_CLIENT`). |
| Test | `core/test_checks.py::test_hosting_region_check`, `compliance/test_no_tracking.py::test_no_external_font_or_image_hosts` |
| Sblocco | Scelta del prestatore UE da parte del committente + attestazione scritta → compilare `DEPLOYMENT.md`, impostare `HOSTING_REGION`. Nessun deploy in questa fase (master prompt §2). |
| Owner | DevOps/Production Readiness Engineer; decisione: committente |

---

## 13. Inventario dei form e dipendenze dai gate

| Form / funzione | Dati personali | Gate | Testo consenso (chiave) | Destinatario e-mail | Note |
|---|---|---|---|---|---|
| Recueil des besoins (imprese) | sì | G2 (← G1), G8 | `p1.companies.form.consent` | `FORMS_RECIPIENT_EMAIL` | 14 campi, ordine vincolato |
| Inscription Forum | sì | G2, G4 (chiuso in PERMANENT), G8 | `p2.forum.registration.consent` | idem | duplicati (evento, e-mail) bloccati |
| Proposition de collaboration (istituzioni / università) | sì | G2, G3 (pagine P3), G8 | testo consenso per finalità "suivi de la présente demande" — **da confermare** (non fornito dal documento → riuso di `p1.companies.form.consent` con `PENDING_CLIENT` per conferma) | idem | link secondario dal Forum attivo già in P2 verso una pagina minimale gated |
| Contact | sì | G2, G8 | come sopra (`PENDING_CLIENT`) | idem | — |
| Newsletter "Restez informés" | sì | G2, G3 | `p3.news.newsletter_consent` | conferma double opt-in all'iscritto | consenso separato, non preselezionato, revocabile |
| Registrazione account / Espace réservé | sì | G2 (Conditions + Privacy), G3 (testi) | accettazione Conditions + Privacy (versioni) | verifica e-mail all'utente | — |
| Wizard di orientamento (anonimo) | no (risposte non identificative, sessione temporanea) | nessuno per l'uso anonimo; G2 per il salvataggio su account | disclaimer `p3.persons.how_it_works` + versione | — | risultato sempre "pré-évaluation à caractère informatif" |
| Forum Virtuale (iscrizione/partecipazione) | sì | G11 (← G1), G2 | Conditions + Privacy | — | profili privati di default |

## 14. Tabella riassuntiva dei gate (stato al 17/09/2026)

| Gate | Nome | Stato | Blocca | Sblocco da |
|---|---|---|---|---|
| G0 | Content lock | ATTIVO (meccanismo) | modifiche non tracciate ai testi | trasmissione scritta |
| G1 | Pagine giuridiche IT | **CHIUSO — BLOCKED_BY_MISSING_OFFICIAL_SOURCE** | pubblicazione testi legali; G2; G11 | Allegato 1 IT |
| G2 | Form pubblici | **CHIUSO** (dipende da G1) | tutti i form con dati personali | automatico da G1 |
| G3 | Phase 3 | **CHIUSO fino al 02/10/2026** | contenuti P3 | data + flag |
| G4 | Forum evento/permanente + banner | APERTO (evento UPCOMING; banner fino al 02/10) | sezioni permanenti prima del 03/10 | automatico |
| G5 | Nomi intervenienti | **CHIUSO** | nomi | programma definitivo scritto |
| G6 | Loghi ufficiali | **CHIUSO** | loghi Regione/Comune | file + autorizzazioni |
| G7 | Marchio ™/® | APERTO su ™ / ® vietato | simbolo ® | comunicazione espressa |
| G8 | E-mail pubbliche | APERTO su contact@agamieuromed.org | indirizzi @legalitalentry.it | attivazione caselle |
| G9 | Analytics | **CHIUSO** (nessun tracking) | qualsiasi tracker | decisione + policy + banner |
| G10 | Traduzioni | FR servito; IT/EN/AR `MISSING` per i testi vincolati | pubblicazione traduzioni non approvate | testi ufficiali |
| G11 | Forum Virtuale | **CHIUSO** | accesso e visibilità | dopo 30/10 + G1 |
| G12 | Hosting UE | **PENDING_CLIENT** | deploy | attestazione scritta |

## 15. Procedura generale di sblocco (checklist)

1. Ricevere il materiale/decisione per iscritto e archiviarne il riferimento (data, mittente, oggetto) — mai nel repository se contiene dati personali.
2. Applicare la modifica **solo** tramite il meccanismo del gate (admin flag con `note`, comando di import, record autorizzato). Mai modificare template o test per "far passare" un gate.
3. Verificare l'`AuditEvent` generato.
4. Eseguire `pytest tests/compliance` e la suite completa.
5. Aggiornare `SiteIdentity.content_version` e la data "Contenus vérifiés le …" nel footer (Impl. p.1).
6. Aggiornare `docs/REQUIREMENTS_MATRIX.md` (colonna Stato) e `docs/QA_REPORT.md`.
7. Commit dedicato con riferimento al gate (es. `gate(G1): publish official Italian legal texts v1.0`).
