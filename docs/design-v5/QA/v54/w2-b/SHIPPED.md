# W2-B shipped — 11 October 2026

**Login «Il varco» and the entrance pages — a living left stage, a premium form.** Tag **`v54/w2-b`** (design-v5
`422a643`, the status commit, as for the earlier families); merge commit `80428a7`. The owner's preview on
http://127.0.0.1:8780 serves it: v5-live checked out at the tag, 8780 restarted at 14:20 and verified. Steward's merge,
label `w2-b-merge`, under `DESIGN_V5_MERGE_LOCK` from 13:28. Reviewed once and fixed (V5.5): `REVIEW.md` and
`A11Y_PERF.md` are both SHIP_AFTER_FIXES with no P0; the fix pass (`NOTES.md`, «Review fixes») closed their findings but
the two handed to the merge — the login's CSS weight, recorded here as measured (DL54-76 item 4), and the production
`collectstatic` (REVIEW M4 = A11Y C1), which stays design-v5's deployment blocker (DL54-76 item 6). No reviewer has read
the fix pass again.

## What shipped

- **The stage answers the person** (`templates/allauth/layouts/entrance.html`, `apps/accounts/static/accounts/entrance.css`,
  `static/css/v5/_door.css`, `static/css/v5/_varco.css`, `static/js/src/entrance.js`): a night niche behind the page's
  light wall, the owner's door on its threshold, four ways in the audiences' colours converging on it, a warm pool at
  the steps' foot. The e-mail field's focus lights the ways; a valid address (read at the typing pause) holds the
  threshold, the pool and the three steps; the password lights the door's frame in the key's gold; on submit the key
  turns once and holds (the loader's own primitive, `data-loader-host="varco-door"`). A state is a function of the form,
  never a memory. The arrival — the four lights travelling into the threshold, 2.4 s, once — plays for a person who
  arrives, never on a refused sign-in, from history, on the phone band or under reduced motion; any gesture cuts it.
  Nothing loops; only transform and opacity move; from the keyboard and under reduced motion the states appear at their
  end; forced colours draw hairlines and steps in the system's ink; without script the stage is the complete rest.
- **The photograph is sharp on a dense screen**: the home's `static/brand/v5` AVIF / WebP set in a `<picture>` whose
  `sizes` is the photo box, preloaded with the same set — one file fetched (the 576 px AVIF at 1440 × 900 @ 2).
- **The form on the paper**: a 25rem column hung from the top of its panel (the title at the same height on every
  entrance page; nothing of the form moves while the page loads), one hierarchy written by the layout — the eyebrow
  «Espace réservé» with the registry's key, ONE title, the page's sentence, the fields «la lastra», ONE flat primary, then
  what is quiet. No placeholder; «Mot de passe oublié ?» at the end of the password's label row (written after the
  control: the keyboard goes address, password, its control, the link, the action); the system's show / hide glyph,
  which keeps the caret and never lets a shown password be spell-checked or corrected (every revealable password of the
  site); the primary of the forms that complete a sign-in holds the loader's key at rest and turns it on submit, the
  label still. Under the action on the sign-in, the FAQ's locked answer on data protection (French; in the other
  languages the FAQ's link alone).
- **Every unhappy state, drawn**: a refusal said once by the summary (focused, both fields described by it, the address
  kept, the title «Erreur — …»), a field's own error, too many failed attempts, too many requests (`templates/429.html`,
  in the request's language, no countdown, the way back), an unverified address (the session message in the form's
  column), the second factor, the reset and its expired link, the new password, an inactive account, signup closed.
- **The same layout** on the sign-up, the password reset (form, sent, bad key, done), the address verification (sent,
  bad link), the inactive account, the second factor and the re-authentication. Below 64rem the stage is a band above
  the form (the door and the help line). In Arabic the page mirrors, the drawing never; the password's room is on its
  control's side.
- **allauth's forms with their presentation only** (`apps/accounts/forms.py`, `ACCOUNT_FORMS`, `MFA_FORMS`): the sign-in
  (`username` as the address's purpose, no placeholder, the e-mail keyboard, left to right), the reset, the new
  password, the second factor's code (the digits' keyboard) and the sign-up's name (`autocomplete="name"`, WCAG 1.3.5).
  Authentication, validation, the rate limits and CSRF are allauth's, untouched; a test holds that no method of the
  sign-in is overridden.
- **What left the cascade**: `components.css` §27's entrance rule; the V4 form rules of `entrance.css`; the second copy
  of the key's mask (`v5/loader.css` now reads `--key-mask` from the door stage's token block).

## The merge

- **The pre-merge sync.** The branch took design-v5 first (`041e056`; design-v5 was `1c001e6`, 38 commits ahead: W3-A's
  console shell, its steward's merge and shipped note). Two conflicts in prose, both areas kept — the decision log
  (below) and DS 2026 §2.1 (the console entry's row is W3-A's, the entrance's row this family's) —, and two dist files,
  not resolved by hand: `static/css/dist` and `static/js/dist` deleted and rebuilt (`npm run build`) on the merged
  sources. `static/css/v5/tokens.css` merged clean and was read: W3-A's two scroll-edge tokens, then §4.2 the hero
  (W2-D), §4.3 the door stage (this family, with `--key-mask`).
- **Numbering.** W3-A's fifteen entries and the record of their merge hold DL54-58 … DL54-73 on design-v5, so the
  family's two entries are **DL54-74** (the stage) and **DL54-75** (the form) — add 16 —, content unchanged but for their
  cross-references and their numbering sentences. The code and DS 2026 cite none of the moved numbers; `NOTES.md`'s
  closing section says how to read the old numbers in the notes, the review and the accessibility report (`d7d0499`).
  The steward's record of the merge is **DL54-76** (`415b21a`, item 2 completed in `7d3d39c`).
- **Ownership.** `scripts/check_ownership.py w2-b design-v5` listed the five paths the family declares; each was read in
  the diff and written under w2-b (`dcf3269`): `static/css/v5/_varco.css` and
  `templates/allauth/elements/form__entrance.html` whole, `static/js/src/shell.js` §3, `static/css/v5/loader.css` §3 and
  `tests/frontend/test_loader_rules.py` as slices; the slices of `apps/accounts/forms.py`, `config/settings/base.py` and
  DS 2026 named as written. After it: 15 inside, 11 slice, 17 generated, and the two steward-only paths the steward
  writes itself — the manifest and the capture report (before: 5 outside).
- **`MFA_FORMS` agreed** (DL54-76 item 3): the second factor's code without a placeholder, on the digits' keyboard —
  allauth's form otherwise.
- **Bundles** rebuilt from a clean `static/js/dist` and `static/css/dist` in the branch (in the sync commit) and in
  design-v5 after the merge (`43fe8b9`; the shared chunks take that worktree's names, every CSS bundle byte for byte the
  branch's). `scripts/regen_design_inventory.py --write` rewrote two figures in the branch (`3ebda2d`: `v5/tokens.css`
  62.2 KB, `v5/loader.css` 11.5 KB) and one after the capture run (§13), and finds design-v5 current after the merge.
- **The capture report** was regenerated on the new login (`2bac1bc`; `docs/qa/design/capture.py` on lane 7, DEBUG off,
  one headless Chromium, the run complete, exit 0): the same 43 captures, none failing a condition; 13 differ, all of
  them the login's (its pages at 390, 768 and 1440 px in French and Arabic, the focused field, the form's errors, the
  200 % and 400 % zooms) and only in the count of icons laid out — two more on each, the eyebrow's key and the
  show / hide glyph: **995 icons laid out** for 969, 0 empty. After an invalid sign-in the focus is on the error summary
  in both languages, as before. DS 2026 §13 follows.
- **Bytes** (gzip −9; DL54-76 items 4 and 5): `dist/main.css` 42 531 B (+79: the door stage's token block),
  `dist/accounts/entrance.css` 4 861 B (+3 879) — **47 392 B in the two sheets every entrance page loads**, 3 949 B over
  their total at `v54/w1-c` (43 443 B) and 1 698 B over the login's Wave-1 allowance (45 694 B). Recorded as measured,
  under V5.5's performance rule and the area's check against W1-0 (LCP 220–320 ms earlier in all four cells, the
  first-render task 46–85 ms where V4's was 384–485, CLS ≤ 0.023): the login page type's ceiling is 47 392 B from here.
  The 79 B of `main.css` reach every page type — the console page types 50 007 → 50 086 B, written into DL54-76 as
  DL54-73 asks; the home 57 182 B, under its ceiling of 59 137 B. `dist/entrance.js` 1 663 B (new, on the entrance pages
  only), `dist/shell.js` 1 131 B (+98). `main.css` stands 3 549 B under its 45 KB ceiling.
- **Lint.** `ruff check` passes on every Python file the area changed; `ruff check .` reports the six findings design-v5
  already has (W1-D's `apps/accounts/apps.py`, `scripts/gen_loader_light.py`), none from this area.
- **Tests** (lane `test_ile_v5_l7`, one pytest at a time). On the branch after the sync and the steward's commits,
  non-browser — `apps/accounts` (the allauth flows, with `test_login_form_w2_b.py`), `tests/security`, `test_layout.py`,
  `test_429_w2_b.py`, `test_css_bundle_is_current`, `test_frontend_bundle_is_current`, `test_design_docs`,
  `test_entrance_w2_b.py`, `test_entrance_form_w2_b.py`, `test_loader_rules.py`, `test_v5_tokens.py`,
  `test_components_w1_c.py`, `test_o14_lint.py`, W3-A's `test_console_shell_w3_a.py` and
  `test_console_shell_stylesheets.py`, `tests/i18n/test_rtl_static.py` and the source parts of the RTL and loader files,
  `tests/test_check_ownership.py`, `tests/test_regen_design_inventory.py`: **1 138 passed**, 0 failed (13 min 5 s).
  Browser (headless Chromium) — `tests/i18n/test_rtl_browser.py`, `test_rtl_browser_entrance.py`, `test_loader_w1_d.py`,
  `test_layout.py`, `test_entrance_w2_b.py`, `test_entrance_form_w2_b.py`, `test_429_w2_b.py`, `apps/accounts`: **111
  passed**, 0 failed, no run crashed (13 min 13 s). After the capture report and the record's last line:
  `test_design_docs`, the inventory and ownership tests and `tests/security` — **212 passed**. On design-v5 after the
  merge and the rebuild: the two bundle tests, `test_design_docs`, the ownership and inventory tests, the tokens, the
  loader's rules, the entrance's two source files, the 429 and the sign-in form's tests — **705 passed** (2 min). Not run:
  the full suite (V5.5: the integration checkpoint). Logs: `C:/tmp/ile_v5_council/evidence/v54/w2-b/merge/`.
- `live_status.json`: the family row w2-b — state v5, its review as the decision, the tag — and the five entrance
  surfaces the census names (`login`, `signup`, `password-reset`, `password-reset-done`, `email-verification-sent`)
  marked v5 with the tag. `CHANGELOG_V54.md`: the entry first.

## On http://127.0.0.1:8780 (all 200, no traceback, after the restart)

- http://127.0.0.1:8780/fr/ · http://127.0.0.1:8780/ar/ · http://127.0.0.1:8780/__design-v5/ — the strip names
  `v54/w2-b`; the index lists the family as passed, with its review
  (http://127.0.0.1:8780/__design-v5/decisioni/w2-b/REVIEW.md), and the five entrance pages as «V5 — council-passed».
- **The sign-in «Il varco»**, signed out («Sortir» in the strip if a persona is in):
  http://127.0.0.1:8780/fr/compte/login/ — load it for the arrival; click the address (the ways light), type a valid
  address and pause (the threshold, the pool and the steps), click the password (the door's frame), press «Afficher le
  mot de passe» (the glyph; the caret stays where it was), then submit a wrong password (the summary first and focused,
  the address kept, the stage at the still of the kept address, no arrival). In Arabic:
  http://127.0.0.1:8780/ar/compte/login/; Italian and English: http://127.0.0.1:8780/it/compte/login/,
  http://127.0.0.1:8780/en/compte/login/ (the assurance is the FAQ's link alone).
- **The other entrance pages**: http://127.0.0.1:8780/fr/compte/signup/, http://127.0.0.1:8780/fr/compte/password/reset/,
  http://127.0.0.1:8780/fr/compte/password/reset/done/, http://127.0.0.1:8780/fr/compte/confirm-email/ — and their
  `/ar/` twins.
- **The phone**: the strip's phone frame, or a window under 1024 px — the band with the door above the form. **Reduced
  motion** (the system's setting): the states without travel, no arrival.
- The second factor, the re-authentication and the 429 need a sign-in in progress or a rate limit reached: they are held
  by the area's tests, not provoked on the owner's server.

Checked after the restart, by request only (no browser on the owner's server;
`C:/tmp/ile_v5_council/evidence/v54/w2-b/merge/verify_8780.log`): `/fr/`, `/ar/`, `/it/`, `/en/`, `/__design-v5/`, the
index and the review answer 200, and the strip names `v54/w2-b`; the sign-in in fr, ar, it and en, the sign-up and the
password reset in fr and ar, the reset's «sent» page and the verification's «sent» page — each 200, with the stage
(`data-varco-stage`, the door's `<picture>` on the v5 AVIF set) and the form in the markup, the sign-in's form naming
the stage (`data-loader-host="varco-door"`), the address with `autocomplete="username"` and no placeholder; the bundles,
the photograph and the grain answer 200; no traceback in the server's log.

## Not done

- **The production `collectstatic`** (REVIEW M4, A11Y C1; DL54-76 item 6) still fails under
  `CompressedManifestStaticFilesStorage`, now on two raw entries — W1-D's console entry and this area's
  `apps/accounts/static/accounts/entrance.css`, whose imports (`../../../../static/css/v5/_door.css`, `…/_varco.css`)
  and `url("../../../../static/img/grain.svg")` leave `STATIC_ROOT` once the raw entry is collected. Nothing a person sees
  depends on it (every template loads the bundle), but no deployment passes that command and 8782 cannot be rebuilt.
  The one correction for both entries — the imports and the `url()` in the static namespace with an `import-rule`
  resolver in `scripts/build_css.mjs`, or the raw entries kept out of `collectstatic` — touches the build script and the
  console's entry: the steward's infrastructure, before the integration milestone.
- **DL54-44 item 2's two forward corrections** (DL54-76 item 7): `hero.css` importing `_door.css` waits for the
  static-namespace import (it would be a third raw entry); `v4/hero.css` leaving `main.css` (≈ 0.6 KB gzip on every
  page) with `templates/components/doorway.html` needs one measured pass on the entrance and on the home's key, which
  still carries `doorway__key` — the deletion map gives the file to W2-D, and the pass lands through the steward.
- **The re-authentication's two forms** (`ACCOUNT_FORMS["reauthenticate"]`, `MFA_FORMS["reauthenticate"]`) still write
  allauth's placeholder, which the sheet does not draw: the same one-line subclass, not asked by the review.
- **Words waiting for the owner (B1)** — the copy packet in `NOTES.md` step 2: a Caps Lock hint, a session-ended line, the
  words of a long wait («Ouverture…», «C'est plus long que d'habitude.», «Réessayer»: until they exist the form is given
  back at 10 s with no retry offered), the second factor's hint and the way to a recovery code, the way forward after
  too many failed attempts, a line for a verification asked too often; and allauth's own strings for one reading (in
  Arabic «يلغي» for «Annuler», the singular address).
- **The skip link still targets `main`** (`templates/base.html`, W1-A's): the first content of `main` is the form's eyebrow
  and title, so the next stop is in the form.
- **The stage's help line** takes its place again when its address is parsed (0.0007 once in forty loads at CPU × 4):
  named for the stage's next pass.
- **Other families'** (the notes): W1-A — `static/css/v5/base.css` still holds `:lang(ar) .entrance .form-field__help`,
  which matches nothing; `docs/ACCESSIBILITY.md` gap G-10 (2.5.8, «Mot de passe oublié ?») is closed on the entrance by
  the label row (24 px, 44 under a finger) — its row, §9's sentence and the checklist's 2.5.8 are to rewrite, and §6
  still shows the help as a `<p>`; W1-C — the system's show / hide control is drawn without script too, where it does
  nothing (the entrance hides it under `html.no-js`; `v5/field.css` could), and the password's room in Arabic on the
  password pages outside the entrance (`v4/buttons.css`'s `padding-inline-end` on a field that is `direction: ltr`);
  W2-C1 — the public navigation is the source of the entrance's load-time shifts (≤ 0.023) and, without script at
  390 px, is laid out open above every page's content; go-live — allauth's e-mails sign with the Sites framework's name
  («example.com» on the lanes' clones): the production site's row to check.
- **Not checked at the merge:** no browser on 8780 (by rule) — the entrance pages were checked there by request only;
  Safari, Firefox, a real phone, a screen reader and a password manager filling `username` were never run (the area's
  notes).
- **The full suite** was not run (V5.5: the integration checkpoint runs it).
