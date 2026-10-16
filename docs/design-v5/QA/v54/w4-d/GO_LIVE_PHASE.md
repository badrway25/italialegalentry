# The go-live phase and the date gates — W4-D, part 1, item 3

Release engineering pass `w4d1-build`, branch `v54-w4-d` (from `design-v5` at `0a8351b`), 16 October 2026. Brief: plan
§3.6 item 4 («the interim-phase variant of the chrome and the hero, if the go-live phase needs it») and the execution
plan's risk 18 / O39 («the Forum date has passed, so the interim's Forum CTA is stale»). Corrected the same day by the
review fixes (`w4d1-fix`, `REVIEW_PART1.md` m5 and its nits): §1 accounts for every gate and says what was checked of
the preview's date; §2.1 names the Forum page's action card.

**Method.** Every page named below was rendered through the real views with Django's test client, on the database a
deployment starts with — `migrate`, then `seed_all`, and no flag row written by anyone — under a frozen clock at five
moments: 16 October 2026 10:00 (the release), 29 October 10:00 (the Morocco Forum, Casablanca), 30 October 20:00
(Rabat, evening), 31 October 00:30 (the first night after, still the 30th in UTC) and 15 December 23:30 (the sixtieth
day), Europe/Rome. Then the same with the owner's documented schedule switched on. French and Arabic. Every internal
link the probed pages show was followed: 113 distinct links with the defaults, 161–167 with the owner's schedule — all
answered 200 or 302. `tests/compliance/test_go_live_calendar_w4_d.py` keeps the result (three tests, one of them a
control that finds the registration button while registration is open).

**Verdict.** Nothing to build and nothing to fix in code: every dated call to action already switches itself off — the
home's Forum banner by its activation window, the Forum's registration by the event's end, the Phase 3 pages by gate
G3 — and no countdown exists anywhere in the product. What is stale is words and one editorial switch, both the
owner's: the Forum page after its event (F-1, F-2). Two findings outside the date: the Virtual Forum's dependency on the
legal pages is displayed but not enforced (F-3), and the sign-in page invites to a closed sign-up (F-4).

## 1. What reads a date or a phase flag

The gates are functions of `apps/core/gates.py` over flags (`apps/core/flags.py`: a database row, else
`settings.FEATURE_FLAG_DEFAULTS`, else off; a flag is active when it is enabled and the clock lies inside its
`[enabled_from, enabled_until)` window). The back-office's phase console (`apps/core/phases.py`) describes each one.

| Gate / flag | What decides it | Date | A fresh deployment | 16 Oct → 15 Dec 2026 | Who moves it |
|---|---|---|---|---|---|
| G1 legal pages | the five official Italian legal documents published (`legal.services.all_official_pages_published`) | none | **closed** (Annex 1 not received) | closed | the owner: the official texts imported and published |
| G2 public forms | G1, or the flag `forms_override_without_legal` (DANGER, audited) | none | **closed** | closed: every form shows «Formulaire temporairement indisponible. Ce formulaire sera activé dès la publication des informations sur le traitement des données personnelles.»; the sign-up «Inscriptions fermées» | automatic with G1 |
| G3 Phase 3 | flag `phase3_public`: default off, `enabled_from` 2 October 2026 00:00 | 2 Oct | **closed**: the interim variant | closed; its date condition holds since 2 October, the switch is the owner's explicit authorisation | the owner (phase console) |
| G4a home banner | flag `forum_banner`: default on, `enabled_until` 2 October 2026 00:00 | until 2 Oct | expired | **hidden every day** | none needed |
| G4b Forum mode | flag `forum_permanent_mode`: default off, `enabled_from` 2 October 2026 18:00; or the edition's `mode_override` (auto / event / permanent) | from 2 Oct 18:00 | **event mode** | event mode — «the date alone must not switch without the flag» (`apps/forum/tests/test_forum_mode.py`); the console: «La transizione è una decisione editoriale, non tecnica, e va presa dopo l'evento» | the owner (F-2) |
| Forum registration | `ForumEvent.registration_is_open()`: event mode **and** `registration_open` **and** not ended (2 October 18:00) **and** before `registration_deadline` **and** under `capacity` | 2 Oct 18:00 | closed | **closed whatever the flags** | none |
| G5 speakers' names, G6 logos | written authorisations (`SpeakerRole`, `ForumPartner`) and a flag | none | closed | functions only, no logo | the owner |
| G11 Virtual Forum | flag `virtual_forum`: default off | documented «after the Morocco Forum (29–30 October 2026)»; no code reads that date | **closed** | closed unless the owner switches it | the owner (F-3) |
| newsletter | flag `newsletter` (row seeded off, `enabled_from` 2 October); its form is under G2 | 2 Oct | closed | closed | the owner |
| `reserved_area_public_link`, `analytics` | flags | none | on / off | unchanged | — |
| Publication windows | `publish_at` / `publish_until` of CMS rows: the hero's Phase 3 variant, the Espace Personnes pathways and the ecosystem's Phase 3 spaces are SCHEDULED for 2 October 2026 | 2 Oct | live in their window, shown only while G3 is open | the moment G3 opens, they show | — |
| `ILE_REFERENCE_DATE` | `core.clock.now()` returns that day at 12:00 Europe/Rome — **only with DEBUG on**; `config/settings/prod.py` forces DEBUG off | — | ignored | ignored | — |

The gates the table does not name read neither a date nor a phase flag: G0 (the content lock), G7 (™/®), G8 (the
public addresses), G10 (the translations) and G12 (EU hosting). G9 (analytics) is only the `analytics` default above,
which no code reads. `docs/LEGAL_AND_PUBLICATION_GATES.md` names flags for G7, G8 and G9
(`trademark_registered_symbol`, `legalitalentry_mailboxes_active`, `analytics_enabled`) that no code reads either.

Dates the settings hold that no code reads: `PHASE1_DEADLINE` (17 September), `PHASE2_DEADLINE` (25 September),
`FORUM_ROVIGO_DATE` (2 October), `FORUM_MOROCCO_DATES` (29–30 October). Nothing changes on 29 or 30 October by itself.

Other reads of the clock show no call to action: the console's deadlines (`clock.today()`; «Mes échéances»), documents'
due dates, retention purges, signed links' expiry, «© {% now "Y" %}» in the footer (computed), the optional «contenus
vérifiés le …» (empty by default), and the FAQ's «Mis à jour le 14.09.2026» (the locked source's date, Phase 3 only).

**`ILE_REFERENCE_DATE` and the preview.** The production-like measuring server runs with
`ILE_REFERENCE_DATE=2026-10-03` (its settings file, outside the repository), and the V5.4 plan (§2.8) gives the preview
server the same date — not checked on the running preview, which this pass does not touch. Every dated transition
happened on 2 October, so 3 October gives the same gate states as every day from 16 October to 15 December: that date
is representative of the window. The preview's flags are not — its database is a QA copy, where flags were set by
hand; a fresh deployment starts as §2.1 describes.

## 2. What a visitor sees, 16 October → 15 December 2026

The states do not change inside the window: every moment rendered the same pages.

### 2.1 A fresh deployment — nobody touches a flag

- **Home** (interim variant, G3 closed): the eyebrow «Orientation · Formation · Mobilité régulière», the title «Un
  écosystème pour les parcours réguliers vers l'Italie», the actions «Découvrir le questionnaire d'orientation» and
  «Espace entreprises»; the four entrances; the orientation passage; the pathways («Les fiches détaillées des parcours
  seront publiées progressivement dans l'Espace Personnes.»); «Ce que fait la plateforme, et ce qu'elle ne fait pas»;
  the ecosystem. **No Forum banner** (its window ended on 2 October) and **no Forum call to action**: O39's dated
  secondary action was never built into V5's hero — the interim's secondary action is the companies' space. The bar:
  «Accueil · Personnes · Entreprises · Forum Vénétie–Maroc · Projet · Contact». The footer: «© 2026 … v2.0.0 — Fase 1».
- **Doors.** Personnes → the interim page (200), «Les fiches détaillées des parcours réguliers vers l'Italie seront
  publiées progressivement dans cet espace.» Entreprises → open (Phase 1), its form unavailable (G2). Institutions and
  Universités & Formation → the entrances lead to the collaboration forms, unavailable (G2); their spaces and the Projet
  Pilote answer 404 (G3), and no page links to them.
- **Forum** — event mode for an event that has taken place: the eyebrow «Événement institutionnel», the title «FORUM
  VÉNÉTIE–MAROC», the fact line «Rovigo — 2 octobre 2026 — Sala della Gran Guardia — 15h00–18h00», the programme, the
  speakers' functions; the registration chapter «La participation est gratuite, sur inscription préalable. Les
  inscriptions sont closes.»; **no registration button**; the page's one action card, «Participer et collaborer»: its
  primary «MANIFESTEZ VOTRE INTÉRÊT POUR LE PROJET PILOTE» (to the companies' form, unavailable under G2) and its
  secondary «PROPOSEZ UNE COLLABORATION». The page's index keeps
  its «INSCRIPTION» entry, a link to the chapter that says it is closed. Three prescribed sentences still speak of the
  event in the future (F-1). Not visible: the page's schema.org `Event` (start 2 October 2026, `EventScheduled`) —
  accurate data about a past event, which search engines stop showing once it is past; it leaves with the permanent
  mode. `/forum/inscription/`: «Les inscriptions sont closes.»
- **Project pages** (le projet, AGAMI, le réseau, contact): no date; the contact form unavailable (G2).
- **Sign-in**: no date. allauth's sentence «Si vous n'avez pas encore créé de compte, merci de vous enregistrer au
  préalable.» links to the sign-up, which answers «Inscriptions fermées — Nous sommes désolés, mais les inscriptions
  sont actuellement fermées.» (F-4).
- **Console** (a person with no case file yet): «Votre prochaine action — Le questionnaire d'orientation», «Mes
  échéances — Les dates qui vous sont communiquées par l'équipe apparaîtront ici.», «Dernière connexion : …» (the
  visit's own time). Nothing dated is offered.
- **Arabic**: the same states; the Forum's dated line stays in French, marked `lang="fr"`.

No past-dated call to action, no countdown (none exists in `templates/`, `apps/` or `static/js/src/`), no «inscriptions
ouvertes» that has closed, no phase that shows nothing: empty chapters hide, the news and partners pages say they are
empty, and every link answers.

### 2.2 The owner's documented schedule

Phase 3 authorised (`phase3_public`), the Forum switched to its permanent mode after the event
(`forum_permanent_mode`), the newsletter flag on, and the Virtual Forum from 31 October (`virtual_forum`) —
`docs/DEPLOYMENT.md` §3 item 10 and the phase console.

- **Home**: the Phase 3 variant — «ITALY LEGAL ENTRY™», «Le parcours régulier vers l'Italie, de l'orientation à
  l'intégration.», the pilot's stations, the FAQ excerpt, «ATTENTION AUX FRAUDES», the reserved area. No banner.
- **Doors and project pages**: Institutions, Universités & Formation, Projet Pilote and the FAQ open; the FAQ's entries
  carry «Mis à jour le 14.09.2026» — the source's date, a fact.
- **Forum** (permanent): «Espace permanent de dialogue et de coopération», «FORUM PERMANENT VÉNÉTIE–MAROC»,
  «Rencontre de lancement : Rovigo — 2 octobre 2026 — …» — the date as the launch meeting's, which is right; no
  registration chapter, no `Event` markup. The permanent collections (results, interventions, media, documents,
  agreements, partners, next meetings) hide while empty: on a fresh database the page is the presentation, the
  programme and the speakers' functions, with the three future-tense sentences of F-1.
- **From 31 October, with `virtual_forum`**: the Forum page gains «FORUM VIRTUEL — … L'accès se fait sur inscription.
  ACCÉDEZ AU FORUM VIRTUEL», and `/forum-virtuel/` opens with «ACCÉDEZ AU FORUM VIRTUEL» and «Créer un compte» — while
  the sign-up is closed and the access request answers that the forms are closed (F-3).
- **News**: «Aucune actualité publiée pour le moment.» and «Restez informés» with the unavailable form (G2).
- **Sign-in** (Phase 3): the FAQ's locked answer «Mes données sont-elles protégées ? Oui. … conservées sur des serveurs
  dans l'Union européenne …» with «Lire la Privacy Policy», which opens the blocked legal page (G1). Not a date; the
  EU-hosting sentence rests on the written confirmation the checklist asks for (A-24).

## 3. Findings

| # | Page and string | What it needs | Whose |
|---|---|---|---|
| F-1 | `/forum/`, both modes: «Au cours du Forum seront également présentés Italy Legal Entry et le projet pilote Vénétie–Maroc.» (`p2.forum.what.body`); «Le programme détaillé des interventions est en cours de définition et sera mis à jour sur cette page.» (`p2.forum.programme.note`); «Sont prévues, entre autres, les interventions d'un Sénateur de la République, … Les noms des intervenants seront publiés avec le programme définitif.» (`p2.forum.speakers.body`); in event mode also «La participation est gratuite, sur inscription préalable.» (`p2.forum.registration.intro`) above «Les inscriptions sont closes.» | new prescribed words for after the event (locked texts: a written transmission, G0) — or keep them as the record of the launch meeting | owner |
| F-2 | `/forum/` presents the past launch event as «Événement institutionnel» while `forum_permanent_mode` is off | switch the permanent mode at the deployment (back-office: the flag `forum_permanent_mode`, or the edition's «mode de la page» = permanent) — existing words only; recommended | owner, at deployment |
| F-3 | `/forum-virtuel/` and the Forum page's teaser, if `virtual_forum` is switched on before the legal pages: «Créer un compte» leads to «Inscriptions fermées»; «L'accès se fait sur inscription.» | until enforced, do not switch `virtual_forum` before G1 (G11's own rule, `docs/LEGAL_AND_PUBLICATION_GATES.md`). The phase console lists `legal_pages_available` as the dependency of `virtual_forum_enabled` and `newsletter_enabled` and says a closed dependency blocks the flag, but `core.gates` reads the flag alone. The fix — both functions also require `legal_pages_available()` — changes what the tests that switch these flags on must set up (the community and forum-governance fixtures, the Forum mode and W3-F2 page tests, the navigation test): a targeted fix with those tests, not this pass | team (fix lane) · owner (meanwhile) |
| F-4 | `/compte/login/`: «Si vous n'avez pas encore créé de compte, merci de vous enregistrer au préalable.» while the sign-up says «Inscriptions fermées» (G2) | hide allauth's invitation while the sign-up is closed; W2-B's sign-in deliberately inherits allauth's block (`templates/account/login.html`), so the change is a template decision of that page, not a date gate | team |
| F-5 | `/forum/` in event mode after the event: the schema.org `Event` | nothing: accurate, ignored once past, gone in permanent mode | — |

**The go-live phase.** Which phase production opens in is the owner's authorisation of Phase 3, not a date: G3's date
condition has held since 2 October. Both variants exist in V5 — the hero (`templates/pages/home/_hero.html`,
`data-hero-variant`: the interim draws the path, the origins and the door; the Phase 3 variant adds the pilot's
stations) and the chrome (the bar's entries follow the gates through `cms_nav`) — and are tested (`apps/pages/tests`,
including the browser tests). The interim-phase variant of plan §3.6 item 4 therefore needs no build, and O39's stale
Forum action cannot occur: no Forum action exists in either hero.
