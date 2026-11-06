# V5.18 stabilisation — lane B (`v518-b-fix`)

29 October 2026 · branch `v518-b` from design-v5 `238dc1c` · worktree `C:/tmp/ile_wt/v518-b` · lane server 8784 (dev
settings, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`, database `ile_v5_l4`) · tests on `test_ile_v5_l4`.
Binding: `directives/V5_18_FINAL_VISUAL_ACCEPTANCE_GATE.md` («Do not use stabilisation as an excuse for another broad
redesign»), V5.15, V5.12, V5.17, DECISIONS §10.0. Audit: `evidence/v518/AUDIT_resp.md`, `AUDIT_quality.md`,
`workflows_v515/v518_findings.json`.

Scope: P10, P-2, P-5, the w3-b test ownership crossing (DL54-174), and T3's stale test in lane B's family
(`test_dashboard_browser_w3_b`, c-rise). Nothing else was changed.

## Fixes

| Id | What the owner saw | Fix | Files |
|---|---|---|---|
| **P10** | Arabic text at 12 px: the «اختياري» tag (`.form-field__optional`) on the needs form and the institutions form, the step numeral (`.steps-head__tile`) at 390 | `:lang(ar)` takes the Arabic caption (`--t-caption`, 14 px under `:lang(ar)` in tokens.css, DL A7/A25). Latin sizes unchanged | `static/css/v5/_formwork.css`, `static/css/v5/_steps.css` (dist `core/forms.css` 5 520 B gzip ≤ 6 KiB, `core/steps.css` 2 327 B) |
| **P-5** | «Mes documents» empty: a bare paragraph and two text links | The empty register renders `components/empty_state.html`: title «Aucun document» (existing msgid, translated), the same sentence (`EMPTY_REGISTER`), the `document` glyph, and «Déposer un fichier hors exigence» as its action when the account may deposit. The page's aside no longer repeats the deposit link when the register is empty («Registre complet» stays). No surface: the F1 rule «never a dashed box» holds | `templates/documents/partials/register.html`, `templates/portal/documents.html` (one condition; lane D's file, crossing recorded), `templates/documents/index.html` (same condition) |
| **P-2** | Account and security pages: allauth's H1, a sentence and a button, 0 animations | (1) **The atrium head**: in the console frame every account page opens on lane D's atrium (the arcade figure, the space's eyebrow, the page's one h1; the space's wash: `person`, `company`, `institution`, `university`). allauth's title element on the manage layout (`h1__manage.html`) draws it when `account_in_console` (set by `_console.html`); the profile and the deletion request draw it through the same partial; the public frame is unchanged. (2) **Motion**: the atrium's own finite draw, and the account column rises with the console's `c-rise` (420 ms, 12 px, 60 ms steps; the head and its h1 never fade; nothing under reduced motion or `html.rm`). (3) **The 2FA page**: `templates/mfa/index.html` recomposes allauth's page — the authenticator block adapts 21st «Enable 2FA Card» (5751): the `shield`/`shield-check` glyph tile, the title with its state chip («activée»/«non activée», the profile's words and registers), allauth's sentence, the three numbered steps on a hairline route (install, scan, enter the code) while it is off, one primary «Activer» (or the danger «Désactiver» when on). Recovery codes and WebAuthn blocks are allauth's, unchanged. Flows, URLs and forms untouched | `apps/accounts/templatetags/account_head.py` (new), `templates/accounts/partials/account_head.html` (new), `templates/allauth/elements/h1__manage.html` (new), `templates/allauth/layouts/_console.html`, `templates/accounts/profile.html`, `templates/accounts/delete_request.html`, `templates/mfa/index.html` (new override), `static/css/v5/_conto-console.css` (new partial, imported by `cms/servizio.css` only — never `cms/errori.css`) |

The rise is written in lane B's account sheet against the console's own `c-rise` keyframes (console.css), not as an
edit of lane A's `_motion.css`: the audit's route («add the wrapper to the `:is()` list through A») would have made the
atrium's h1 rise too. Lane A may fold it into `_motion.css` later; the values are the same.

## The w3-b test ownership crossing (DL54-174)

Lane D's resolution in `test_the_consoles_empty_state_spans_the_main_column` let the class on the page choose the rule
(`if reg-calm … else …`): on Communications the surfaceless branch was never exercised. **Corrected, not weakened**:
the test is now parametrised by register and holds each to its own, named rule — Communications draws lane D's calm
panel (`.reg-calm`, spans the main column); «Mes demandes» and «Mes documents» (P-5) draw lane B's empty-state tile
(`.empty-state`: start edge, reading measure, no surface). It also asserts exactly one empty state per page and that
the page draws the expected kind. Both rules stand, as the steward confirmed; the Director's question (which empty
state governs the platform registers) is unchanged.

## T3 — the stale c-rise guard (lane B's family test `test_dashboard_browser_w3_b`)

`moving` now admits the console's `c-rise` only when it is finite, on the document timeline, and **finished** before
the measurement (its `both` fill keeps a finished rise in `getAnimations()`). A running c-rise, an infinite one and every
other animation still fail; the reduced-motion tests still require `getAnimations().length == 0`. The same predicate
serves the bridge's `moving` count. `SETTLE_JS` now also awaits a finite c-rise (≤ 2.5 s) — the company dashboard's
column is outside lane D's `[data-platform]`, so its rise was still running at the measurement.
Uncovered once c-rise was admitted: the person's dashboard at 390 fr counted a fourth corner, `12px` — the step chip
«Étape 1 sur 7 — Votre situation et votre objectif» wraps to two lines, and v5/chip.css keeps its one-line pill radius
on purpose (review m2: «the pill on one line, a plate on two»). The radii probe counts a `.chip` as the pill; every
other corner still counts. The bridge's four section failures (`[deadlines, messages, organisation]`) are lane
D's tree and are not touched.

## New msgids (for lane D's catalogue pass — no .po edited)

`Installez une application d’authentification` · `Sur votre téléphone, une application qui génère des codes à usage
unique.` · `Scannez le code QR` · `La page d’activation affiche un code QR propre à votre compte : l’application
l’enregistre.` · `Saisissez le code` · `Le code affiché par l’application confirme l’activation.`
Until then each sentence still in French carries `lang="fr"` (`ui_lang`) and `dir="auto"` (it/en/ar), and
`tests/i18n/test_catalogues.py::test_every_source_message_is_in_the_catalogue[it|en|ar]` and
`::test_audit_script_succeeds_with_full_coverage` are red on this branch (green on design-v5): they ask for exactly
this catalogue pass (`scripts/i18n_audit.py --sync`, the renderings below, `--compile`). Lane B does not edit the
`.po` (DECISIONS §10.0: lane D's).

Lane B's renderings for the pass (provisional, the institutional registers of I18N_RTL §4–§5: Italian «Lei», Arabic
the formal plural; nothing machine-translated):

| msgid | it | en | ar |
|---|---|---|---|
| Installez une application d’authentification | Installi un’applicazione di autenticazione | Install an authenticator app | ثبّتوا تطبيقًا للمصادقة |
| Sur votre téléphone, une application qui génère des codes à usage unique. | Sul Suo telefono, un’applicazione che genera codici monouso. | On your phone, an app that generates one-time codes. | على هاتفكم، تطبيق يولّد رموزًا صالحة لاستعمال واحد. |
| Scannez le code QR | Scansioni il codice QR | Scan the QR code | امسحوا رمز QR |
| La page d’activation affiche un code QR propre à votre compte : l’application l’enregistre. | La pagina di attivazione mostra un codice QR proprio del Suo account: l’applicazione lo registra. | The activation page shows a QR code unique to your account: the app saves it. | تعرض صفحة التفعيل رمز QR خاصًّا بحسابكم: يحفظه التطبيق. |
| Saisissez le code | Inserisca il codice | Enter the code | أدخلوا الرمز |
| Le code affiché par l’application confirme l’activation. | Il codice mostrato dall’applicazione conferma l’attivazione. | The code shown by the app confirms the activation. | يؤكّد الرمز الذي يعرضه التطبيق التفعيل. |
Reused (exist, translated): «Aucun document», «Déposer un fichier hors exigence», «activée», «non activée», «Mon
compte», «Supprimer mon compte», the profile lead, allauth's own strings.

## Checked in HEADED Chromium 1234 (lock `v518-b-fix`, 17:13–17:25), lane server 8784

Probes `C:/tmp/ile_v5_council/.work/v518-b/probe.py`, captures `…/v518-b/shots/` (r1 account + documents, r2 forms,
widths, reduced motion; r3 2FA languages).
- 2FA fr/ar/it/en at 1440 and 390; fr/ar at 1280, 1024, 768, 360; qa-company at 1440/390: one h1, 0 overflow, no text
  under the floor (12 px Latin / 14 px Arabic), steps on the reading start (the right edge in Arabic), the atrium's
  drawing at the reading end (mirrored), the phone band below 48 rem.
- Profil, mot de passe, adresses e-mail fr/ar 1440/390: one h1 each, 0 overflow, no small text.
- Mes documents (qa-fresh-person) fr/ar/it/en 1440/390: the tile on the main column's start edge (right in Arabic),
  no surface, the deposit button 44 px, translated in every language.
- P10: `/xx/entreprises/recueil-des-besoins/` and `/xx/collaboration/institutions/` ar/fr 1440/390: no Arabic text
  under 14 px.
- Reduced motion (2FA, Mes documents): `getAnimations()` empty.

## Tests (lane l4, `test_ile_v5_l4`, `-p no:randomly`)

- Non-browser, `apps/accounts apps/portal apps/documents tests/frontend tests/i18n tests/compliance -m "not browser"`:
  **31 failed, 3 519 passed**. 27 of them fail identically on design-v5 `238dc1c` (run there on the same lane:
  portal `test_requests_empty_state` / `test_pathways_empty_state…`, `test_login_invitation_w4_d` ×3,
  `test_service_pages_w3_f2` ×10, `test_routing` ×4, `_fronte.css` ×2, `test_design_docs` gradients (m-6),
  `test_journey_w3_d`, `test_mobile_rtl_w4_a`, `test_o14_lint` (lane A's header `check`), `test_v5_tokens`). The 4 new
  ones are the catalogue's (`test_catalogues` ×4): the six new msgids above, for lane D's pass.
  `test_o14_lint::…persons_own_choice` gains the 2FA page's `shield-check` seat (DECISIONS §4, the same meaning as the
  profile's); it stays red only for the pre-existing `templates/partials/header.html` `check`.
- After the last changes: `test_design_docs test_css_bundle_is_current test_static_pipeline test_css_tokens_exist
  test_rtl_static test_o14_lint test_icons test_account_shell_v512_b apps/accounts apps/documents test_v5_tokens
  test_rm_flag_parity` — 1 263 passed, 5 failed, all pre-existing.
- Browser (headless Chromium from the tests, lock held): `test_dashboard_browser_w3_b` **25 passed, 4 failed** (the
  bridge's sections, lane D — was 22 + 4 failing and the empty-state test unparametrised);
  `test_service_pages_browser_w3_f2`, `test_browser_w1_b` pass; `test_content_pages_browser_w3_f2::…grammar…` still red
  only on corners and shadows (the orchestrator's V5.15 admissions) — **no «text too small» left** (P10).

## Refix after the integrated review (`v518-b-refix`, 29 October 2026)

- **Polish (lane b, `static/css/v5/_conto-console.css:36`)**: the account column's `c-rise` took fill `both`, against
  lane A's V5.18 rule «backwards, never both» (`_motion.css`): with `both` the finished rise kept its transform, so each
  column child stayed a containing block. Now `backwards`. Nothing else changed; `static/css/dist/cms/servizio.css`
  rebuilt (`npm run build:css`; only that bundle moved).
- Headed Chromium 1234 (lock `v518-b-refix`, 19:57–19:58), lane server 8784, `qa-doc-person`: 2FA and Profil, fr/ar,
  1440 and 390, plus reduced motion at 1440. At load every column `c-rise` reports fill `backwards` (3 on 2FA, 5 on
  Profil); 1.6 s later none is left in `getAnimations()`, every child's computed `transform` is `none` and opacity 1;
  one h1, 0 overflow, no page error; the 2FA steps unmoved (left 659 fr / 738 ar at 1440; 16 / 331 at 390). Reduced
  motion: no animation. Probe and captures: `C:/tmp/ile_v5_council/.work/v518-b-refix/` (`probe.py`, `probe.json`,
  `shots/`).
- Tests (`test_ile_v5_l4`, `-p no:randomly`): `test_design_docs test_css_bundle_is_current test_account_shell_v512_b`
  51 passed, 1 failed (the `_platform.css` gradients, m-6, pre-existing); `test_service_pages_w3_f2` 39 passed, 10
  failed (the same 10 as above); browser `test_service_pages_browser_w3_f2 test_browser_w1_b
  test_overlays_console_w2_a test_account_shell_v512_b` 23 passed.
- `test_dashboard_browser_w3_b`'s note on a `both` fill describes lane A's dashboard rise (`_motion.css`), not this
  sheet; left as it is.
- Lock incident: at 20:01 a failed `noclobber` acquire was followed by an unconditional `rm`, which removed
  another session's `CHROMIUM_LOCK` (its label was not read). No Playwright Chromium was running at that moment; the
  next acquire was guarded and released only on this lane's own label (20:01–20:04).
