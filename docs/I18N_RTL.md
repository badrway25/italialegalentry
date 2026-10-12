# I18N & RTL — Italy Legal Entry™

Documentazione **di ciò che esiste nel codice** al 20/09/2026: architettura a quattro lingue, modello delle
lingue dei contenuti, flusso di traduzione, glossario terminologico, regole RTL, checklist di verifica con
file e test, difetti aperti e corretti (seconda revisione indipendente: 20/09/2026). Ogni tabella di questo
documento è verificata da
`tests/i18n/test_documentation.py` (percorsi citati, test citati, glossario ↔ cataloghi, screenshot).

Owner: RTL/i18n Specialist — `locale/`, `scripts/i18n_audit.py`, `tests/i18n/`, questo documento.
Documenti collegati: `docs/ARCHITECTURE.md` §4.5, `docs/LEGAL_AND_PUBLICATION_GATES.md` (G10),
`docs/DESIGN_SYSTEM.md`, `docs/ACCESSIBILITY.md`, ADR-004 (francese lingua sorgente).

---

## 1. Architettura a quattro lingue

| Elemento | Implementazione | Test |
|---|---|---|
| Lingue | `LANGUAGES = it, fr, en, ar`; `LANGUAGE_CODE = "fr"` (sorgente e fallback, ADR-004); `RTL_LANGUAGES = {"ar"}`; `CONTENT_FALLBACK_LANGUAGE = "fr"` — `config/settings/base.py` | `tests/i18n/test_routing.py::test_settings_describe_the_four_language_architecture` |
| URL | `i18n_patterns(..., prefix_default_language=True)` in `config/urls.py`: ogni pagina pubblica vive sotto `/it/`, `/fr/`, `/en/`, `/ar/`; un percorso senza prefisso è **reindirizzato**, mai servito; `/de/…` → 404 | `tests/i18n/test_routing.py::test_a_path_without_language_prefix_is_redirected_never_served` |
| Radice `/` | `core.views.root_redirect`: cookie `ile_language` → `Accept-Language` → `fr` | `tests/i18n/test_routing.py::test_root_redirects_to_the_negotiated_language`, `tests/i18n/test_routing.py::test_language_cookie_wins_over_the_browser_language` |
| Middleware | `LocaleMiddleware` dopo `SessionMiddleware` e prima di `CommonMiddleware`; header `Content-Language` su ogni risposta | `tests/i18n/test_routing.py::test_every_ungated_public_route_renders_in_the_language` |
| Cookie di lingua | `LANGUAGE_COOKIE_NAME = "ile_language"`, `SameSite=Lax`, `Secure` in produzione (`HttpOnly` quando lo scrive il middleware); cookie **tecnico** (nessun consenso richiesto). Lo scrivono `POST /i18n/setlang/` (`django.views.i18n.set_language`, protetto da CSRF, nessun redirect esterno, un `GET` non cambia nulla) e `core.middleware.LanguageCookieMiddleware` (`apps/core/middleware.py`): quando una pagina con prefisso di lingua è servita con successo il cookie viene allineato al prefisso — mai su un 404, mai per un prefisso non pubblicato, mai riscritto se già uguale | `tests/i18n/test_routing.py::test_set_language_view_stores_the_cookie_and_translates_the_url`, `tests/i18n/test_routing.py::test_set_language_refuses_an_external_redirect_and_changes_nothing_on_get`, `tests/i18n/test_routing.py::test_set_language_is_csrf_protected`, `tests/i18n/test_routing.py::test_only_technical_cookies_are_set_when_browsing_in_arabic`, `tests/i18n/test_page_integrity.py::test_language_cookie_is_only_written_for_a_published_language_and_a_served_page` |
| Selettore di lingua | `templates/components/language_segmented.html`: controllo segmentato di **link** (funziona senza JS) alla stessa pagina nelle quattro lingue (`translate_url` in `core.context_processors.site`), ciascuno con `lang`, `hreflang`, `dir` ed endonimo; `aria-current` sulla lingua attiva. Non è un form: il cookie è scritto dal middleware quando la pagina scelta viene servita (I18N-05, corretto) | `tests/i18n/test_routing.py::test_language_switcher_links_to_the_same_page_in_the_four_languages`, `tests/i18n/test_ui_translations.py::test_language_switcher_is_labelled_in_the_page_language` |
| `<html lang dir>` | `templates/base.html`: `lang="{{ site.lang }}" dir="{{ site.dir }}"`, classe `is-rtl` sul `body`, preload del font arabo solo in RTL | `tests/i18n/test_routing.py::test_every_phase3_route_renders_in_the_language_once_the_gate_opens`, `tests/compliance/test_public_pages.py::test_arabic_is_rtl_and_others_ltr` |
| SEO | `templates/partials/seo_head.html`: `canonical` nella lingua della pagina, `hreflang` per le quattro lingue + `x-default` | `tests/i18n/test_routing.py::test_hreflang_alternates_and_canonical_follow_the_language` |
| Menu | `apps/cms/templatetags/cms_nav.py`: albero costruito sotto `translation.override(lang)`; etichette `MenuItem.label_<lang>` o, in assenza di righe, struttura statica con stringhe gettext | `tests/i18n/test_routing.py::test_menu_links_carry_the_prefix_of_the_page_language`, `tests/i18n/test_ui_translations.py::test_skip_link_header_and_navigation_are_translated` |
| Pagine senza prefisso | `/documents/…`, `/backoffice/`, `/api/`, `sitemap.xml`, `robots.txt`: lingua da cookie → `Accept-Language`; il cookie segue la lingua letta sul sito, quindi chi naviga in arabo con un browser francese trova `/documents/` in arabo | `tests/i18n/test_page_integrity.py::test_language_neutral_pages_follow_the_language_cookie`, `tests/i18n/test_page_integrity.py::test_language_chosen_by_browsing_is_kept_on_language_neutral_pages` |
| E-mail | rese al momento dell'accodamento (`notifications.services.queue_email`), quindi nella lingua della richiesta; le notifiche interne alla casella unica (`templates/notifications/email/enquiries_*.txt`) restano in francese di proposito | `tests/i18n/test_ui_translations.py::test_visitor_emails_are_rendered_in_the_language_of_the_request` |

---

## 2. Modello delle lingue dei contenuti

Tre famiglie di testo, tre regole diverse. **Nessuna** prevede traduzione automatica.

| Famiglia | Dove vive | Chi traduce | Resa nelle altre lingue |
|---|---|---|---|
| **Testi prescritti** (documento di implementazione) | `apps/cms/locked_content.py` (`LOCKED_TEXTS["fr"]`, checksum in `apps/cms/locked_content.sha256.json`) | **nessuno del team**: solo versioni ufficiali trasmesse dalla committente, aggiunte a `LOCKED_TEXTS["it" / "en" / "ar"]` con `scripts/lock_content.py` | francese con `lang="fr"`: `{% locked "chiave" %}` → `<span lang="fr">…</span>`; `{% locked "chiave" "h1" "classe" %}` → `lang` sull'elemento |
| **Pagine legali** (5 documenti) | `apps/legal` — testo ufficiale **italiano** (Allegato 1), gate G1 | nessuno | `<article lang="it">` in tutte le lingue; la riga di stato è interfaccia e segue la lingua della pagina |
| **Contenuti CMS** (FAQ, glossario, notizie, schede, percorsi, partner…) | modelli con `cms.models.TranslationBase` (`master`, `language`, `status`, `source`, `reviewed_by`) | redazione, con revisione | solo le righe `PUBLISHED` sono pubbliche (`cms.translation.resolve`); altrimenti sorgente francese con `lang="fr"` — gate **G10** |
| **Interfaccia** (navigazione, pulsanti, etichette, messaggi, stati vuoti, errori, back-office) | gettext, sorgente **francese**: `{% translate %}`, `{% blocktranslate %}`, `gettext_lazy` | il team, nei cataloghi `locale/<lang>/LC_MESSAGES/django.po` | vedere §2.1 |

### 2.1 Copertura reale, al 21 settembre 2026

| Catalogo | msgid | tradotti | non tradotti | fuzzy | copertura |
|---|---:|---:|---:|---:|---:|
| `it` | 3618 | 3618 | 0 | 0 | **100 %** |
| `en` | 3618 | 3618 | 0 | 0 | **100 %** |
| `ar` | 3618 | 3618 | 0 | 0 | **100 %** |
| `fr` | 3618 | 3618 | 0 | 0 | **100 %** |

I moduli di piattaforma aggiunti il 21/09 avevano introdotto **1664 msgid** assenti dai cataloghi:
documenti, imprese, selezione, academy, sportello, fascicolo, notifiche e workspace del Forum erano
partiti in solo francese, e la copertura era scesa al 54 %. Sono stati tradotti, una corsia per
lingua, con `scripts/i18n_audit.py` come criterio d'accettazione — segnaposto e tag identici al
msgid, sei forme plurali in arabo, cifre occidentali, nessuna formulazione vietata, marchio e nomi
delle policy verbatim.

Il catalogo `fr` ha inoltre ricevuto **67 normalizzazioni**: msgid scritti in italiano dal codice di
back-office, che senza traduzione francese avrebbero mostrato l'italiano sul sito francese.

Stati di `TranslationBase.status`: `missing` → `draft` → `reviewed` → `approved` → `published`
(`cms.models.TranslationStatus`). `cms.translation.translation_matrix(obj)` alimenta la colonna «Stato per
lingua» del back-office (`missing` dove la riga non esiste).

Garanzie verificate:

| Garanzia | Test |
|---|---|
| Il tag `{% locked %}` aggiunge `lang="fr"` solo fuori dal francese | `tests/i18n/test_locked_texts.py::test_locked_tag_renders_french_with_a_lang_attribute`, `tests/i18n/test_locked_texts.py::test_locked_tag_needs_no_lang_attribute_in_french` |
| Una tabella di lingua del registro contiene solo chiavi ufficiali; il resto ricade sul francese | `tests/i18n/test_locked_texts.py::test_registry_falls_back_to_french_without_an_official_version` |
| Nessun catalogo traduce un testo prescritto | `tests/i18n/test_locked_texts.py::test_no_catalogue_translates_a_locked_text`, `tests/i18n/test_catalogues.py::test_no_unreviewed_locked_fragment_in_the_catalogue` |
| Le pagine reali mantengono il testo prescritto francese con `lang="fr"` | `tests/i18n/test_locked_texts.py::test_companies_page_keeps_the_prescribed_french_wording`, `tests/i18n/test_locked_texts.py::test_forum_page_keeps_the_prescribed_french_wording`, `tests/i18n/test_locked_texts.py::test_phase3_hero_keeps_the_prescribed_french_wording` |
| Il testo legale ufficiale è italiano in ogni lingua | `tests/i18n/test_locked_texts.py::test_official_legal_text_is_italian_in_every_language` |
| Il markup di fallback non finisce mai in `<head>` o in un attributo | `tests/i18n/test_page_integrity.py::test_fallback_markup_never_leaks_into_head_or_attributes` |

**Regola per i template**: in un attributo o nel `<title>` il testo prescritto va reso **senza markup**:
`{% locked "chiave" as testo %}{{ testo|striptags }}` (come `templates/pathways/index.html`). La forma
`{{ testo }}` senza filtro stampa `<span lang="fr">` dentro l'attributo nelle pagine it / en / ar (I18N-02, corretto;
protetto da `tests/i18n/test_page_integrity.py::test_fallback_markup_never_leaks_into_head_or_attributes`).

**Regola per i valori di fallback** (WCAG 3.1.2 «lingua delle parti»): un valore mostrato in una lingua diversa
da quella della pagina — titolo prescritto francese, termine giuridico italiano, valore CMS senza traduzione
pubblicata — deve portare il proprio `lang`, anche quando passa da un componente: `breadcrumbs` e `local_nav`
accettano una chiave opzionale `lang` (`templates/components/breadcrumbs.html`,
`templates/components/local_nav.html`), `cms.locked_content.text()` restituisce un `LockedText` con
`fallback_lang` (letto dai componenti quando la voce non indica `lang`). Senza `lang` il lettore di schermo usa la voce sbagliata e `static/css/base.css` non può isolare
il testo da sinistra a destra nelle pagine arabe. Test su ogni pagina araba (route pubbliche, riepilogo errori di
un form, area riservata): `tests/i18n/test_page_integrity.py::test_latin_text_on_arabic_pages_carries_its_own_lang_attribute`
(I18N-08, corretto — §9.1).

---

## 3. Flusso di traduzione — redazione

1. **Contenuto CMS**: scrivere il sorgente francese; aprire la scheda «Traduzioni» dell'oggetto; creare la riga
   della lingua (`draft`); far rivedere (`reviewed` → `approved`, campo `reviewed_by`); pubblicare
   (`published`). Finché la riga non è `published` il sito mostra il francese marcato `lang="fr"`.
2. **Testo prescritto o legale**: la redazione **non** lo traduce. Quando la committente trasmette una versione
   ufficiale, uno sviluppatore la inserisce nel registro (tabella della lingua), rigenera i checksum con
   `scripts/lock_content.py` e il diff è revisionato. Nel campo `source` delle righe CMS collegate si annota
   la trasmissione («testo ufficiale trasmesso il …»).
3. **Voci di menu**: `cms.MenuItem` ha un'etichetta per lingua (`label_it`, `label_fr`, `label_en`,
   `label_ar`); se `label_ar` è vuota viene mostrata quella francese. La descrizione del mega-menu è solo
   francese (`description_fr`): usarla con parsimonia finché non esiste il campo per lingua.
4. **Mai**: traduzione automatica di testi prescritti/legali, nomi di persone istituzionali, promesse di
   esito, il simbolo ®. Il marchio è sempre `Italy Legal Entry™`.

## 4. Flusso di traduzione — sviluppo

1. Scrivere la stringa **in francese** con `{% translate %}` / `{% blocktranslate %}` / `gettext_lazy`.
   A livello di modulo (costanti, attributi di classe, valori di default) **solo** `gettext_lazy`: il `gettext`
   immediato viene valutato una volta, all'import, nella lingua attiva in quel momento, e tutti i visitatori
   leggono quella (I18N-07). Verificato su ogni modulo di `apps/`:
   `tests/i18n/test_page_integrity.py::test_no_module_level_constant_is_translated_at_import_time`.
   Tipografia francese nel sorgente (`’`, `« »`, spazio prima di `:`); le traduzioni usano la tipografia
   della propria lingua (`«…»` it, `“…”` en, `«…»` ar, nessuno spazio prima dei due punti).
2. Sincronizzare i cataloghi: `.venv/Scripts/python scripts/i18n_audit.py --sync` (equivalente puro Python
   di `makemessages`: aggiunge i msgid nuovi con `msgstr` vuoto, elimina quelli non più usati, non tocca
   le traduzioni esistenti). Su una macchina con GNU gettext si può usare
   `manage.py makemessages -l it -l en -l ar --ignore=.venv --ignore=staticfiles --ignore=docs --add-location=file`;
   su questo host Windows `xgettext`/`msgfmt` non sono installati. Non esistono stringhe JS (`djangojs` non serve).
3. Tradurre **tutte e tre** le lingue nel `.po` (UTF-8, nessun `fuzzy`, tutte le forme plurali: it 2, en 2,
   ar 6). Rispettare il glossario del §5.
4. Compilare: `.venv/Scripts/python scripts/i18n_audit.py --compile` (scrive i `.mo` in puro Python) e
   verificare che l'audit esca con codice 0.
5. Eseguire `pytest tests/i18n` (i test browser richiedono Chromium di Playwright).

Il catalogo `locale/fr` non traduce: normalizza in francese i pochi msgid scritti in italiano (stringhe di
back-office) e dichiara la regola plurale francese.

### 4.1 Cosa controlla `scripts/i18n_audit.py`

| Controllo | Esito se fallisce |
|---|---|
| per lingua: msgid, tradotti, non tradotti, fuzzy, obsoleti, copertura | exit 1 sotto il 100 % o con un fuzzy |
| intestazioni `Language`, `charset=UTF-8`, `Plural-Forms` (it 2, en 2, fr 2, ar 6) e ogni indice plurale compilato | exit 1 |
| nessun msgid duplicato (GNU `msgfmt` lo rifiuta; il compilatore puro Python terrebbe l'ultimo in silenzio) | exit 1 |
| segnaposto (`%(name)s`, `%s`, `{name}`) e tag HTML inline identici tra msgid e msgstr | exit 1 |
| nessuna formulazione vietata (`cms.forbidden`), nessun mojibake, nessuna cifra arabo-indica, voci arabe scritte in caratteri arabi | exit 1 |
| **«™» seguito da U+200E** in ogni frase araba (e dopo il segnaposto `%(project)s`) — §7.4 | exit 1 |
| nessun msgid con un frammento di testo prescritto (6 parole consecutive): ogni sovrapposizione è giustificata in `REVIEWED_OVERLAPS` o congelata in `KEEP_SOURCE` (msgstr = msgid in tutte le lingue) | exit 1 |
| sincronizzazione catalogo ↔ sorgenti (template e Python) | exit 1 con l'elenco dei msgid mancanti |
| `.mo` identico al `.po` voce per voce (confronto di contenuto, mai di date) | exit 1 |
| catalogo `fr`: nessuna frase con msgid italiano rimasta identica al msgid (`--sync` copia il msgid nuovo come testo francese: giusto per le stringhe francesi, sbagliato per le poche stringhe di back-office scritte in italiano) | exit 1 |

Test: `tests/i18n/test_catalogues.py::test_audit_script_succeeds_with_full_coverage`,
`tests/i18n/test_catalogues.py::test_audit_fails_on_an_untranslated_or_locked_msgid`,
`tests/i18n/test_catalogues.py::test_audit_fails_on_an_arabic_trademark_without_the_left_to_right_mark`,
`tests/i18n/test_catalogues.py::test_every_source_message_is_in_the_catalogue`,
`tests/i18n/test_catalogues.py::test_sync_adds_new_messages_and_drops_unused_ones`,
`tests/i18n/test_catalogues.py::test_pure_python_compiler_round_trips`,
`tests/i18n/test_catalogues.py::test_audit_fails_on_an_italian_msgid_copied_into_the_french_catalogue`,
`tests/i18n/test_catalogues.py::test_audit_fails_on_a_duplicate_msgid`.

### 4.2 Registri linguistici

| Lingua | Registro |
|---|---|
| Italiano | istituzionale, forme impersonali («È possibile…», «Inserire…») o infinito; niente anglicismi evitabili («Accedi», «Carica», «Pannello di riepilogo»); restano «account», «password», «e-mail», «partner» come nell'uso della PA |
| Inglese | britannico istituzionale sobrio (`organisation`, `authorised`, `anonymised`), «Individuals» per *Personnes*, «Enterprises» per *Entreprises* |
| Arabo | arabo standard moderno, registro istituzionale con lessico amministrativo marocchino (`التكوين`, `المسطرة`, `التوصل`), plurale di cortesia (`كم`), cifre occidentali, nomi propri latini invariati |

Non si traducono: `Italy Legal Entry™`, `AGAMI — Dialogo Giuridico Interculturale APS`, `Privacy Policy`,
`Cookie Policy`, `Vénétie–Maroc`, l'indirizzo `contact@agamieuromed.org`, i termini giuridici italiani del
glossario (`tests/i18n/test_catalogues.py::test_proper_nouns_trademark_and_policy_names_stay_verbatim`).

---

## 5. Glossario terminologico

Decisioni terminologiche vincolanti: una modifica qui è una decisione, non un refuso. La tabella è
confrontata con i tre cataloghi da `tests/i18n/test_documentation.py::test_glossary_table_matches_the_catalogues`;
i termini fondamentali sono anche in `tests/i18n/test_catalogues.py::test_glossary_terms_keep_their_approved_translation`.

> **Non ancora trascritto.** I moduli della piattaforma hanno introdotto termini che le tre corsie
> di traduzione hanno risolto in modo coerente nei cataloghi ma che non sono ancora righe di questa
> tabella: *pièce* (distinto da *document*), *processus de sélection*, *mandat*, *besoin*, *acteur
> autorisé*, *commission*, *table thématique*, *relation annuelle*, *jalon*, *guichet numérique*,
> *référent*. Finché non sono qui, non sono vincolanti: il prossimo traduttore può discostarsene
> senza che nulla lo segnali. Trascriverli richiede la resa nelle tre lingue per ciascuno, e il test
> sopra rifiuta una riga che non corrisponda al catalogo — quindi è un lavoro da fare con le tre
> corsie, non da improvvisare qui.

| Français (source) | Italiano | English | العربية |
|---|---|---|---|
| Accueil | Pagina iniziale | Home | الرئيسية |
| Personnes | Persone | Individuals | الأفراد |
| Entreprises | Imprese | Enterprises | الشركات |
| Institutions | Istituzioni | Institutions | المؤسسات |
| Universités & Formation | Università e Formazione | Universities & Training | الجامعات والتكوين |
| Universités et organismes de formation | Università e organismi di formazione | Universities and training bodies | الجامعات وهيئات التكوين |
| Espace Personnes | Area Persone | Individuals Area | فضاء الأفراد |
| Espace Entreprises | Area Imprese | Enterprises Area | فضاء الشركات |
| Espace réservé | Area riservata | Reserved area | الفضاء الخاص |
| Actualités | Notizie | News | الأخبار |
| Projet | Progetto | Project | المشروع |
| Projet pilote | Progetto pilota | Pilot project | المشروع التجريبي |
| Réseau | Rete | Network | الشبكة |
| Contact | Contatti | Contact | اتصل بنا |
| Partenaires | Partner | Partners | الشركاء |
| Le promoteur du projet | Il promotore del progetto | The promoter of the project | الجهة المبادِرة بالمشروع |
| Votre parcours | Il proprio percorso | Your pathway | مساركم |
| Parcours réguliers | Percorsi regolari | Regular pathways | المسارات النظامية |
| Diplômes et titres | Diplomi e titoli | Diplomas and qualifications | الشهادات والمؤهلات |
| Formation | Formazione | Training | التكوين |
| Vivre en Italie | Vivere in Italia | Living in Italy | العيش في إيطاليا |
| Attention aux fraudes | Attenzione alle frodi | Beware of fraud | احذروا الاحتيال |
| Questions fréquentes | Domande frequenti | Frequently asked questions | الأسئلة الشائعة |
| Glossaire | Glossario | Glossary | مسرد المصطلحات |
| Questionnaire d’orientation | Questionario di orientamento | Orientation questionnaire | استبيان التوجيه |
| Pré-évaluation | Prevalutazione | Preliminary assessment | التقييم الأولي |
| Besoins professionnels | Fabbisogni professionali | Professional needs | الاحتياجات المهنية |
| Recueil des besoins | Raccolta dei fabbisogni | Needs collection | رصد الاحتياجات |
| Forum Virtuel | Forum Virtuale | Virtual Forum | المنتدى الافتراضي |
| Se connecter | Accedi | Sign in | تسجيل الدخول |
| Se déconnecter | Esci | Sign out | تسجيل الخروج |
| Créer un compte | Crea un account | Create an account | إنشاء حساب |
| Mon compte | Il mio account | My account | حسابي |
| Tableau de bord | Pannello di riepilogo | Dashboard | لوحة المتابعة |
| Mes demandes | Le mie richieste | My requests | طلباتي |
| Mes documents | I miei documenti | My documents | وثائقي |
| Mon parcours | Il mio percorso | My pathway | مساري |
| Mes échéances | Le mie scadenze | My deadlines | آجالي |
| Communications | Comunicazioni | Communications | المراسلات |
| Informations légales | Informazioni legali | Legal information | المعلومات القانونية |
| Mentions légales | Note legali | Legal notice | الإشعارات القانونية |
| Conditions d’utilisation | Condizioni di utilizzo | Terms of use | شروط الاستخدام |
| Avertissement | Avvertenze | Disclaimer | تنبيه |
| Aller au contenu principal | Vai al contenuto principale | Skip to main content | الانتقال إلى المحتوى الرئيسي |
| Retour à l’accueil | Torna alla pagina iniziale | Back to the home page | العودة إلى الصفحة الرئيسية |
| Fil d’Ariane | Percorso di navigazione | Breadcrumb | مسار التنقل |
| Choisir la langue | Scegli la lingua | Choose language | اختيار اللغة |
| Suivant | Successivo | Next | التالي |
| Précédent | Precedente | Previous | السابق |
| Enregistrer | Salva | Save | حفظ |
| Rechercher | Cerca | Search | بحث |
| Téléverser | Carica | Upload | رفع |
| Envoyer la demande | Invia la richiesta | Submit the request | إرسال الطلب |
| Consentement | Consenso | Consent | الموافقة |
| Formulaire temporairement indisponible. | Modulo temporaneamente non disponibile. | Form temporarily unavailable. | النموذج غير متاح مؤقتًا. |
| Page en cours de préparation. | Pagina in corso di preparazione. | Page under preparation. | الصفحة قيد الإعداد. |
| Page introuvable | Pagina non trovata | Page not found | الصفحة غير موجودة |

«Forum Vénétie–Maroc» resta tale in it / en; in arabo «منتدى Vénétie–Maroc» (nome proprio latino invariato).
«Privacy Policy» e «Cookie Policy» restano in originale in ogni lingua, come sul sito.

---

## 5bis. Governance del rule engine — termini decisi il 22 settembre 2026

Risolti dalle quattro corsie sulle diciotto stringhe nuove della catena di governance.

**Non sono righe vincolanti della tabella §5**, e la differenza è concreta: il test
`test_glossary_table_matches_the_catalogues` legge solo le righe dentro §5 e le confronta con i tre
cataloghi. Spostarle lì è una decisione da prendere con chi ha tradotto, non da fare di passaggio —
ed è anche la ragione per cui questa tabella sta **fuori** da §5 e non come sua sottosezione: messa
dentro, sarebbe diventata vincolante senza che nessuno lo avesse deciso.

| Italiano (sorgente) | Français | English | العربية |
|---|---|---|---|
| Fonte verificata | Source vérifiée | Source verified | تم التحقق من المصدر |
| Candidata — contenuto ereditato | Candidate — contenu hérité | Candidate — inherited content | مرشَّحة — محتوى موروث |
| provenienza del contenuto | provenance du contenu | provenance of the content | منشأ المحتوى |
| Redatta dalla fonte normativa | Rédigée à partir de la source normative | Drafted from the legislative source | محرَّرة انطلاقًا من المصدر القانوني |
| Ripresa dalla piattaforma precedente | Reprise de la plateforme précédente | Carried over from the previous platform | مأخوذة عن المنصة السابقة |
| verificata da | vérifiée par | verified by | المتحقِّق منه |
| approvata da (registrato) | approuvée par (enregistré) | approved by (recorded) | المصادِق عليها (مسجَّل) |

Tre scelte che meritano di essere ricordate, perché sono decisioni e non sinonimi:

- **`legislative source`, non `legal source`.** In inglese `legal source` è già preso dal modello
  `LegalSource` («fonte giuridica»). Tenerli distinti impedisce all'etichetta di provenienza di
  leggersi come se nominasse il record della fonte.
- **`giurista`, non `avvocato`.** Prima occorrenza della parola nel catalogo italiano. «Avvocato»
  restringerebbe a chi è iscritto all'albo; la revisione può farla un giurista che non lo è.
- **`review workflow`, non `review process`.** La stringa nomina la macchina a stati
  `LEGACY_CANDIDATE → SOURCE_VERIFIED → LEGAL_REVIEW → APPROVED → ACTIVE`, non una prassi informale.

Il catalogo francese ha avuto qui un criterio d'accettazione diverso dagli altri. `--sync` riempie
una voce nuova copiando il msgid, il che è corretto per un msgid francese e sbagliato per i sedici
italiani: `msgid "Fonte verificata"` si è ritrovato `msgstr "Fonte verificata"`. È esattamente il
difetto che il catalogo `fr` esiste per impedire, e la copertura non poteva vederlo — contava 100 %
su sedici traduzioni che traduzioni non erano.

---

## 6. Plurali

`Plural-Forms`: it / en `nplurals=2; plural=(n != 1)`, fr `plural=(n > 1)`, ar sei forme
(`0`, `1`, `2`, `3–10`, `11–99`, `100+` secondo CLDR). Le sei forme arabe sono frasi diverse (duale
compreso), non copie: «نتيجتان», «%(counter)s نتائج», «%(counter)s نتيجة»; le forme 0, 1 e 2 possono omettere
il numero. I cataloghi di progetto dichiarano la propria regola e Django la applica ai messaggi del progetto
anche quando il catalogo di Django per la stessa lingua ne dichiara un'altra.

Test: `tests/i18n/test_catalogues.py::test_headers_and_plural_rule`,
`tests/i18n/test_catalogues.py::test_arabic_plural_forms_are_selected_by_django`,
`tests/i18n/test_catalogues.py::test_two_form_plurals_are_selected_by_django`,
`tests/i18n/test_ui_translations.py::test_plural_sentence_is_rendered_through_the_template_tag`
(pagina reale: ricerca nelle FAQ, `{% blocktranslate count %}`).

---

## 7. Regole di implementazione RTL

### 7.1 Solo proprietà logiche
`margin-inline-start`, `padding-inline-end`, `inset-inline-start`, `border-inline-end`, `text-align: start / end`,
`inline-size` / `block-size`. **Mai** `left`, `right`, `margin-left`, `float: left`, `text-align: left`.
Verificato su **ogni** foglio di stile del progetto (`static/css/*.css`, `apps/*/static/**/*.css`):
`tests/i18n/test_rtl_static.py::test_stylesheet_uses_logical_properties_only`.

### 7.2 Trasformazioni orizzontali
`translateX()` non è logica: ogni regola che sposta in orizzontale ha la gemella `[dir="rtl"]` con il segno
invertito (`tests/i18n/test_rtl_static.py::test_every_horizontal_shift_has_its_rtl_twin`). Attenzione:
`transform` **sostituisce**, non somma: per lo spostamento al passaggio del mouse di un'icona specchiata il design
system usa la proprietà individuale `translate` (`translate: -3px 0`), che si compone con lo `scaleX(-1)` di
`.icon--flip-rtl` (RTL-05, corretto); il test riconosce entrambe le scritture
(`tests/i18n/test_rtl_static.py::test_horizontal_shift_detector_reads_the_transform_function_and_the_translate_property`).
Una forma disegnata con bordi logici (`border-inline-end`) è **già** specchiata: non va ruotata una seconda volta
(RTL-08, corretto).

### 7.3 Icone direzionali
Le icone che indicano «avanti» (`arrow`, `chevron-end`) portano la classe `.icon--flip-rtl`
(`static/css/base.css`: `[dir="rtl"] .icon--flip-rtl { transform: scaleX(-1) }`). Non si specchiano: spunta,
lucchetto, ricerca, calendario, busta, telefono, scudo, `arrow-up-right` (link esterno), chevron verticali di
accordion e menu. Test su ogni pagina araba:
`tests/i18n/test_page_integrity.py::test_forward_icons_are_mirrored_on_every_arabic_page`; resa nel browser:
`tests/i18n/test_rtl_browser.py::test_header_breadcrumbs_and_arrows_are_mirrored_semantically`.

### 7.4 Isolamento bidi dei contenuti latini
* `static/css/base.css` mantiene `direction: ltr; unicode-bidi: isolate` per `input[type=email|tel|url|number|password]`,
  `.brand__wordmark`, `.email`, `.phone`, `code`, `time[datetime]` e per la classe di utilità `.ltr`;
  gli input latini restano allineati a destra (`text-align: end`). Test:
  `tests/i18n/test_rtl_static.py::test_bidi_helpers_keep_latin_data_left_to_right`,
  `tests/i18n/test_rtl_browser.py::test_arabic_form_is_right_aligned_and_latin_inputs_stay_ltr`.
* Numeri, date (`d/m/Y`), telefoni ed e-mail si scrivono con **cifre occidentali** anche in arabo (coerenza con
  il resto del sito): `tests/i18n/test_catalogues.py::test_arabic_catalogue_is_arabic_script_western_digits_no_mojibake`.
* **Marchio**: «™» è un carattere bidi neutro; alla fine di una sequenza latina dentro una frase araba prende la
  direzione del paragrafo e viene dipinto a sinistra del nome («™Italy Legal Entry»). Nel catalogo arabo ogni
  «™» (e il segnaposto `%(project)s`, che riceve il marchio) è seguito da **U+200E LEFT-TO-RIGHT MARK**. Il
  carattere è invisibile: copiarlo da una voce esistente; l'audit rifiuta la voce che ne è priva. Test:
  `tests/i18n/test_catalogues.py::test_arabic_trademark_sign_is_anchored_by_a_left_to_right_mark`,
  `tests/i18n/test_rtl_browser.py::test_trademark_sign_stays_on_the_right_of_the_name_in_arabic_sentences`.
* Testo misto generato da variabili (nome utente, riferimento di sessione, titolo di un termine italiano): avvolgerlo
  in `<bdi>` o in un elemento con `lang` e `dir="ltr"`.
* I blocchi di fallback (`lang="fr"`, `lang="it"`, `lang="en"`) dentro una pagina araba sono isolati LTR da
  `static/css/base.css` (`[dir="rtl"] :is(p, h1…h6, li, dd, dt, blockquote, label, td, th, span…)[lang]`): la
  punteggiatura finale del testo prescritto resta al suo posto. Solo gli elementi **di testo** cambiano direzione —
  `label` compreso, perché la frase di consenso prescritta è un `<label lang="fr">` (RTL-09, corretto); contenitori,
  link e pulsanti seguono la pagina, così layout e frecce restano specchiati. **Attenzione agli elenchi puntati
  nativi**: un `<li lang="fr">` isolato LTR disegna il proprio punto elenco a **sinistra**, fuori dal padding
  dell'elenco (che in RTL sta a destra); su un `<li>` con marcatore nativo il `lang` va messo su uno `<span>`
  interno, oppure l'elenco usa `list-style-position: inside` (§9, RTL-10). Test:
  `tests/i18n/test_rtl_browser.py::test_french_fallback_blocks_are_isolated_left_to_right_on_arabic_pages`,
  `tests/i18n/test_rtl_static.py::test_fallback_blocks_in_another_language_are_isolated_left_to_right`.

### 7.5 Tipografia araba

**Aggiornata il 21/09/2026 con l'art direction A.** Prima l'arabo aveva **un solo volto** per tutti e sei
i livelli, mentre il latino aveva una coppia serif/sans: l'edizione araba non aveva quindi alcun contrasto
fra display e testo. Ora l'arabo ha la sua coppia, come il latino:

| Ruolo | Famiglia | Perché |
|---|---|---|
| Display e lettura | **Noto Naskh Arabic** (`--font-display-ar`) | Un vero naskh è il registro dei documenti amministrativi marocchini e la controparte corretta di un serif latino |
| Interfaccia | **IBM Plex Sans Arabic** (`--font-ui-ar`) | Etichette, pulsanti, tabelle e form, dove una costruzione di derivazione cufica è appropriata |

`static/css/tokens.css`, blocco `:root:lang(ar)`: sostituisce `--font-display` e `--font-ui` con le due
famiglie arabe, apre l'interlinea di lettura da 28 a **32 px** (il naskh ha bisogno di spazio per i segni
diacritici, e la dimensione non si riduce), e azzera `--track-folio` e `--track-caps-display` perché il
tracking spezza le legature. Entrambe le famiglie sono self-hosted in `static/fonts/`, senza alcun host
esterno, e la pagina araba precarica **il volto di lettura del proprio alfabeto**, non un serif latino.

Test: `tests/i18n/test_rtl_static.py::test_arabic_has_its_own_display_and_interface_pair`,
`tests/i18n/test_rtl_browser.py::test_arabic_typefaces_are_applied_and_loaded`,
`tests/frontend/test_layout.py::test_html_lang_and_dir_attributes`.

### 7.6 JavaScript
`static/js/main.js` legge `document.documentElement.dir`: nella barra di menu e nelle schede `ArrowLeft`
porta all'elemento **successivo** in RTL. Nessuna stringa visibile è generata da JS (nessun catalogo `djangojs`).

---

## 8. Checklist di verifica RTL

Eseguita con Playwright (Chromium) a **390 px** e **1440 px** su `/ar/` e, per confronto, su `/fr/`:
homepage, form «Recueil des besoins» (gate G2 aperto con testo legale di prova), FAQ (Fase 3 aperta), login,
questionario di orientamento. Screenshot in `docs/qa/rtl/` (`<pagina>-<lingua>-<larghezza>.png`).

| Voce | Implementazione | Test | Esito |
|---|---|---|---|
| Navigazione (desktop, mega-menu) | `templates/partials/header.html`, `static/css/components.css` | `tests/i18n/test_rtl_browser.py::test_desktop_mega_menu_opens_inside_the_viewport` | OK — marchio a destra, menu a sinistra, pannello dentro il viewport |
| Drawer (mobile) | `templates/partials/header.html`, `static/js/main.js` | `tests/i18n/test_rtl_browser.py::test_mobile_drawer_opens_inside_the_viewport` | OK — si apre, si chiude con Esc, nessun overflow |
| Breadcrumb | `templates/components/breadcrumbs.html`, `static/css/components.css` | `tests/i18n/test_rtl_browser.py::test_header_breadcrumbs_and_arrows_are_mirrored_semantically`, `tests/i18n/test_rtl_browser.py::test_breadcrumb_separator_points_forward_in_arabic`, `tests/i18n/test_page_integrity.py::test_latin_text_on_arabic_pages_carries_its_own_lang_attribute` | OK — ordine da destra, separatore «‹» (RTL-08 corretto), titoli francesi e termini italiani con il proprio `lang` (I18N-08 corretto) |
| Form | `templates/components/form_field.html`, `static/css/base.css` | `tests/i18n/test_rtl_browser.py::test_arabic_form_is_right_aligned_and_latin_inputs_stay_ltr` | OK — etichette e controlli allineati a destra, e-mail/telefono LTR |
| Validazione | `templates/components/form_errors.html`, `templates/components/form_field.html` | `tests/i18n/test_rtl_browser.py::test_arabic_form_is_right_aligned_and_latin_inputs_stay_ltr` (`docs/qa/rtl/form-errors-ar-390.png`), `tests/i18n/test_page_integrity.py::test_latin_text_on_arabic_pages_carries_its_own_lang_attribute` | OK — riepilogo errori e messaggi tradotti, etichette prescritte con `lang="fr"`, nessun overflow |
| Frecce | `static/css/base.css` (`.icon--flip-rtl`), `static/css/components.css` | `tests/i18n/test_page_integrity.py::test_forward_icons_are_mirrored_on_every_arabic_page`, `tests/i18n/test_rtl_browser.py::test_mirrored_arrow_stays_mirrored_while_hovered` | OK — specchiate su ogni pagina araba, anche al passaggio del mouse (RTL-04, RTL-05 corretti) |
| Icone non direzionali | `static/img/icons.svg` | `tests/i18n/test_page_integrity.py::test_forward_icons_are_mirrored_on_every_arabic_page` | OK — non specchiate |
| Accordion | `templates/components/accordion.html` | `tests/i18n/test_rtl_browser.py::test_arabic_accordion_opens_with_its_question_at_the_inline_start` | OK — domanda a destra, icona a sinistra |
| Card e sezioni | `templates/components/card.html`, `templates/components/entrances.html` | `tests/i18n/test_rtl_browser.py::test_arabic_pages_do_not_overflow_and_are_captured_with_their_ltr_twin` | OK — griglie specchiate, nessun overflow |
| Tabelle | `static/css/layout.css` (`.scroll-x`), `templates/portal/documents.html` | `tests/i18n/test_page_integrity.py::test_no_french_interface_string_is_visible_in_the_reserved_area` | intestazioni tradotte, scorrimento nel contenitore; nessun test browser dedicato (limite §9) |
| Paginazione | `templates/components/pagination.html`, `static/css/components.css` | `tests/i18n/test_rtl_static.py::test_previous_page_icon_points_backwards_in_both_directions` | OK — «precedente» punta indietro in LTR e in RTL (RTL-07 corretto) |
| Modali | `templates/components/dialog.html`, `static/css/components.css` | `tests/i18n/test_rtl_static.py::test_every_horizontal_shift_has_its_rtl_twin` | OK — `<dialog>` nativo centrato; fallback senza JS centrato senza `transform` (RTL-06 corretto) |
| Stepper / flusso a passi | `templates/components/stepper.html`, `templates/orientation/_step.html` | `tests/i18n/test_rtl_browser.py::test_arabic_orientation_wizard_is_mirrored_on_a_phone` (`docs/qa/rtl/wizard-ar-390.png`) | OK — barra di avanzamento da destra, scelte e pulsanti specchiati |
| Ricerca | `templates/faq/index.html`, `templates/glossary/index.html` | `tests/i18n/test_rtl_browser.py::test_arabic_search_pages_do_not_overflow_on_a_phone` | OK — il form va a capo, nessun overflow a 390 px |
| Date, numeri, telefono, e-mail | `static/css/base.css` (`time[datetime]`, `.email`, `.phone`) | `tests/i18n/test_rtl_static.py::test_bidi_helpers_keep_latin_data_left_to_right` | OK — cifre occidentali, LTR isolato |
| Marchio | `locale/ar/LC_MESSAGES/django.po` (U+200E), `apps/cms/templatetags/cms_nav.py` | `tests/i18n/test_rtl_browser.py::test_trademark_sign_stays_on_the_right_of_the_name_in_arabic_sentences`, `tests/i18n/test_rtl_browser.py::test_trademark_sign_stays_on_the_right_of_the_name_in_every_wordmark` | OK — «™» a destra del nome nelle frasi tradotte e in ogni marchio, footer compreso (I18N-06 corretto) |
| Testi francesi di fallback | `apps/core/templatetags/ile_core.py` (`lang="fr"`), `static/css/base.css` | `tests/i18n/test_rtl_browser.py::test_french_fallback_blocks_are_isolated_left_to_right_on_arabic_pages`, `tests/i18n/test_rtl_static.py::test_fallback_blocks_in_another_language_are_isolated_left_to_right` | OK — elementi di testo `lang="fr"` isolati LTR (frase di consenso `<label>` compresa, RTL-09 corretto), punteggiatura al suo posto |
| Desktop 1440 / mobile 390 | — | `tests/i18n/test_rtl_browser.py::test_arabic_pages_do_not_overflow_and_are_captured_with_their_ltr_twin`, `tests/i18n/test_rtl_browser.py::test_every_arabic_public_page_fits_the_viewport` | OK — `scrollWidth <= clientWidth` e un solo `h1` su **tutte** le route pubbliche in arabo, a 390 e a 1440 px |
| Area riservata (mobile 390) | `templates/portal/base_portal.html`, `apps/portal/static/portal/portal.css` | `tests/i18n/test_rtl_browser.py::test_arabic_reserved_area_fits_a_phone`, `tests/i18n/test_rtl_browser.py::test_arabic_saved_pre_assessment_fits_a_phone` | OK — le undici pagine dell'area riservata e dell'account senza overflow in arabo; **3 px di scorrimento orizzontale** su «Mon parcours» quando esiste una prevalutazione salvata (RTL-10) |
| Interfaccia tradotta ovunque | `locale/` | `tests/i18n/test_page_integrity.py::test_no_french_interface_string_is_visible_on_a_translated_public_page`, `tests/i18n/test_page_integrity.py::test_no_french_interface_string_is_visible_while_every_gate_is_closed`, `tests/i18n/test_ui_translations.py::test_latin_text_in_the_arabic_chrome_is_limited_to_proper_nouns` | OK — 0 stringhe francesi di interfaccia su tutte le route pubbliche (gate aperti **e** gate chiusi, cioè lo stato pubblicato oggi) e nell'area riservata |
| Lingua delle parti | `templates/components/breadcrumbs.html`, `templates/components/local_nav.html`, `templates/components/form_errors.html`, `templates/pathways/detail.html`, `templates/glossary/term.html` | `tests/i18n/test_page_integrity.py::test_latin_text_on_arabic_pages_carries_its_own_lang_attribute` | OK — ogni testo latino delle pagine arabe (route pubbliche, riepilogo errori, area riservata) porta il proprio `lang` (I18N-08 corretto) |

Confronto LTR/RTL (screenshot `home-fr-1440.png` / `home-ar-1440.png` e gemelli): marchio, navigazione, griglie
dei quattro accessi, numerazione dei percorsi, diagramma del progetto pilota, colonne del footer e pulsanti sono
specchiati; le fotografie non vengono ribaltate (corretto: non sono direzionali).

---

## 9. Difetti aperti e limiti noti

Protocollo per un difetto che sta in un file di **altri owner**: un test `xfail` (non `strict`) il cui motivo
inizia con l'ID lo tiene visibile, e una tabella `KNOWN_…` lo esclude dal test principale. Quando l'owner
corregge, il test passa (XPASS): si tolgono allora marcatore e tabella, così il test principale protegge la
correzione, e la riga passa al §9.1. Al 21/09/2026 resta aperto un solo difetto, I18N-04, garantito
dall'audit e non da un `xfail`: nessun difetto RTL aperto porta oggi un marcatore `xfail`. Il difetto
dei punti elenco in fallback latino è stato corretto il 20/09/2026 ed è registrato al §9.1.

| ID | Gravità | Difetto | Owner / file | Correzione richiesta | Test |
|---|---|---|---|---|---|
| I18N-04 | bassa | Tre msgid derivati da testi prescritti restano francesi in ogni lingua (`KEEP_SOURCE` in `scripts/i18n_audit.py`): descrizione del mega-menu «Entreprises» (`apps/cms/templatetags/cms_nav.py`), occhiello del Forum (`templates/forum/partials/hero.html`), meta description di `templates/living/topic.html` | owner dei rispettivi file | riformulare la stringa o renderla dal registro con `{% locked %}` (che aggiunge `lang="fr"`) | `tests/i18n/test_catalogues.py::test_locked_derived_msgids_are_never_translated` |

Limiti noti (non difetti):

* **I testi delle regole giuridiche sono in francese in ogni lingua.** `LegalRule.message_fr` e
  `requirement_fr` sono contenuto di database, non stringhe di catalogo. `LegalRule.message_key`
  esiste proprio per questo e ora **viene letto**: `rules.services.displayed()` usa la traduzione
  della chiave quando esiste e ricade sul francese quando non esiste — mai la chiave stessa, che
  sullo schermo sarebbe peggio del francese. Fornire quattro lingue per regola è lavoro redazionale
  del referente giuridico, non una modifica di codice.
* **Gli endonimi delle lingue** («Français», «Italiano», «English», «العربية») non passano da
  gettext e non devono: un endonimo è il nome che una lingua dà a sé stessa e resta invariato. Sono
  resi con il proprio attributo `lang` (e `dir` per l'arabo), come già faceva il commutatore di
  lingua — `accounts.profile_forms.LanguageSelect`.

* **Contenuti CMS**: FAQ, glossario, percorsi, schede e notizie di seed esistono solo in francese; in it / en / ar
  compaiono in francese con `lang="fr"` finché la redazione non pubblica le traduzioni (G10). I titoli di pagina
  (`<title>`) e le meta description che contengono testo prescritto restano in francese senza `lang`
  (l'attributo non è ammesso in quei punti).
* **Termini giuridici italiani** («Questura», «Nulla osta»…) sono mostrati in italiano in ogni lingua per scelta
  editoriale; nelle liste delle autorità (`templates/pathways/detail.html`) portano il `lang` della propria voce.
* **Cataloghi di terzi**: le stringhe di django-allauth e di Django (login, MFA, validazione dei campi) usano
  le traduzioni dei rispettivi pacchetti; in arabo allauth dà del «tu» (`لديك`) mentre il sito usa il plurale
  di cortesia. Accettato; si può sovrascrivere la singola stringa nel catalogo di progetto.
* **Tabelle e paginazione**: nessun test browser dedicato in RTL (le pagine che le usano richiedono dati e
  login); coperte da test statici e dal test di interfaccia dell'area riservata.
* **Riferimenti `#:` dei `.po`** con backslash (generati su Windows): innocui, ma un `makemessages` su Linux
  li riscrive tutti — usare `scripts/i18n_audit.py --sync` per diff minimi.
* **`AppConfig.verbose_name`** di alcune app non è passato da gettext (solo back-office).
* **Titolo del Forum in modalità permanente** (`apps/forum/services.py`, `_(PERMANENT_TITLE)`): l'argomento non è
  un letterale, quindi non entra nei cataloghi e resta francese in ogni lingua — corretto per un titolo che viene
  dal documento di implementazione, ma va reso con `lang="fr"` quando la modalità permanente sarà attivata.
* **Numeri formattati da JavaScript** (`static/js/main.js`, `Intl.NumberFormat(document.documentElement.lang)`):
  con `lang="ar"` Chromium restituisce cifre occidentali (verificato); altri motori possono scegliere le cifre
  arabo-indiane. Nessun template usa ancora `data-counter`; al primo uso fissare `numberingSystem: "latn"`.
* **Back-office**: interfaccia di amministrazione tradotta (nomi dei modelli, azioni, testi di aiuto), ma
  django-unfold non è verificato in RTL: l'arabo non è una lingua di lavoro della redazione.

### 9.1 Difetti corretti (20/09/2026)

Corretti dal rispettivo owner durante le due revisioni; il test che li teneva visibili come `xfail` è ora un
test di regressione ordinario, e le tabelle `KNOWN_…` corrispondenti sono state eliminate.

| Difetto | Correzione | Test di regressione |
|---|---|---|
| RTL-01 — blocchi di fallback `lang="fr"` che ereditavano `direction: rtl` | regola globale in `static/css/base.css` | `tests/i18n/test_rtl_browser.py::test_french_fallback_blocks_are_isolated_left_to_right_on_arabic_pages` |
| RTL-03 — form di ricerca di FAQ e glossario fuori di 33 px a 390 px | `.search-form` in `static/css/components.css` | `tests/i18n/test_rtl_browser.py::test_arabic_search_pages_do_not_overflow_on_a_phone` |
| I18N-02 — `<span lang="fr">` dentro la meta description (notizie, Vivre en Italie) | `\|striptags` nei template | `tests/i18n/test_page_integrity.py::test_fallback_markup_never_leaks_into_head_or_attributes` |
| I18N-03 — categorie di notizie francesi senza `lang="fr"` | `templates/news/` | `tests/i18n/test_page_integrity.py::test_no_french_interface_string_is_visible_on_a_translated_public_page` |
| I18N-05 — cookie di lingua mai scritto navigando: `/documents/` nella lingua del browser | `core.middleware.LanguageCookieMiddleware` | `tests/i18n/test_page_integrity.py::test_language_chosen_by_browsing_is_kept_on_language_neutral_pages` |
| I18N-06 — «™Italy Legal Entry» nel marchio del footer in arabo | isolamento LTR di ogni marchio `{% brand %}` | `tests/i18n/test_rtl_browser.py::test_trademark_sign_stays_on_the_right_of_the_name_in_every_wordmark` |
| I18N-07 — titoli delle pagine legali bloccate («Note legali», «Condizioni di utilizzo», «Avvertenze») tradotti **all'import** con `gettext` immediato: `<h1>` e `<title>` francesi su it / en / ar (lo stato pubblicato oggi) | `gettext_lazy` in `apps/legal/views.py` | `tests/i18n/test_page_integrity.py::test_blocked_legal_page_titles_follow_the_page_language`, `tests/i18n/test_page_integrity.py::test_no_module_level_constant_is_translated_at_import_time` |
| I18N-08 — valori di fallback senza `lang` sulle pagine it / en / ar (WCAG 3.1.2): titoli prescritti francesi e termini giuridici italiani nel breadcrumb e nella navigazione locale, etichette prescritte nel riepilogo errori dei form, liste delle autorità, fonti del glossario | chiave `lang` opzionale in `templates/components/breadcrumbs.html` e `templates/components/local_nav.html`, `LockedText.fallback_lang` in `apps/cms/locked_content.py`, `<span lang>` in `templates/components/form_errors.html`, `templates/pathways/detail.html`, `templates/glossary/term.html`; le view passano la lingua della voce | `tests/i18n/test_page_integrity.py::test_latin_text_on_arabic_pages_carries_its_own_lang_attribute` |
| I18N-09 — profilo: «Rôles» mostrava i nomi tecnici dei gruppi (`role:person`) | etichette tradotte in `apps/accounts/roles.py` (8 nuovi msgid, tradotti in it / en / ar) | `tests/i18n/test_page_integrity.py::test_profile_page_shows_no_technical_role_identifier` |
| RTL-04 — frecce «avanti» non specchiate nell'Espace Personnes | `icon--flip-rtl` in `templates/pathways/` | `tests/i18n/test_page_integrity.py::test_forward_icons_are_mirrored_on_every_arabic_page` |
| RTL-05 — freccia specchiata che tornava a destra al passaggio del mouse | proprietà `translate` al posto di `transform: translateX()` in `static/css/components.css` | `tests/i18n/test_rtl_browser.py::test_mirrored_arrow_stays_mirrored_while_hovered` |
| RTL-06 — fallback senza JS del dialog decentrato in RTL | centratura senza `transform` | `tests/i18n/test_rtl_static.py::test_every_horizontal_shift_has_its_rtl_twin` |
| RTL-07 — freccia «precedente» della paginazione rivolta in avanti | `.pagination__icon-prev` in `static/css/components.css` | `tests/i18n/test_rtl_static.py::test_previous_page_icon_points_backwards_in_both_directions` |
| RTL-08 — separatore del breadcrumb rivolto verso l'alto in arabo | `rotate(45deg)` nella regola `[dir="rtl"]` | `tests/i18n/test_rtl_browser.py::test_breadcrumb_separator_points_forward_in_arabic` |
| RTL-09 — frase di consenso prescritta (`<label lang="fr">`) disposta da destra a sinistra nei form arabi: il punto finale saltava all'inizio dell'ultima riga | `label` nella regola di isolamento di `static/css/base.css` | `tests/i18n/test_rtl_browser.py::test_french_fallback_blocks_are_isolated_left_to_right_on_arabic_pages`, `tests/i18n/test_rtl_static.py::test_fallback_blocks_in_another_language_are_isolated_left_to_right` |
| RTL-10 — «Mon parcours» in arabo a 390 px: 3 px di scorrimento orizzontale con una prevalutazione salvata; una voce `<li lang="fr">` dentro un elenco specchiato appendeva il punto elenco fuori dal bordo inline-start, a sinistra, dove l'elenco specchiato non ha padding | `static/css/base.css`: `list-style-position: inside` per le sole voci in fallback latino dentro un elenco RTL | `tests/i18n/test_rtl_browser.py::test_arabic_saved_pre_assessment_fits_a_phone` |

---

## 10. Comandi rapidi

```
.venv/Scripts/python scripts/i18n_audit.py                 # rapporto; exit 1 se un controllo fallisce
.venv/Scripts/python scripts/i18n_audit.py --sync          # allinea i .po ai sorgenti (msgstr vuoti da tradurre)
.venv/Scripts/python scripts/i18n_audit.py --compile       # scrive i .mo (puro Python) e rifà l'audit
.venv/Scripts/python scripts/i18n_audit.py --json          # stesso rapporto, leggibile da macchina
.venv/Scripts/python -m pytest tests/i18n -q -p no:cacheprovider
.venv/Scripts/python -m pytest tests/i18n/test_rtl_browser.py   # rigenera docs/qa/rtl/*.png
```
