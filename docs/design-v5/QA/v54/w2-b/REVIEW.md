# W2-B — the login «Il varco» and the entrance pages · senior review (one pass, V5.5)

Italy Legal Entry™ · design V5 · V5.4 plan §1.13, §1.9 (the engage), §3.4 item 2 · DL54-07, 58, 59 · V5.5 delivery mode ·
label **w2-b-review** · 11 October 2026, 10:00–10:55 · branch `v54-w2-b` at `9772c53` (the code at `61c4771`; the commit
after it is the notes), worktree `C:/tmp/ile_wt/v54-w2-b`, on my own server **127.0.0.1:8887** (`ile_v5_l7`,
`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`). I built nothing and wrote nothing but this file. One pass,
design + UX + taste together, against the owner's bar («credible alongside excellent international digital products») and the
settled direction; then the security of an authentication page. Accessibility and performance have their own check: not
repeated here, except where a standing rule is plainly missed.

## Verdict — SHIP_AFTER_FIXES

**No P0.** No broken page, no wrong direction, nothing unusable, no data or security problem: 0 console message, 0 CSP
violation, 0 failed request (beyond the 429 I provoked and one 403 from a probe session that cannot re-authenticate) and
0 px of horizontal overflow on every page and state I loaded (fr, ar, it, en; 1440 × 900, 1366 × 768, 1024 × 768,
390 × 844, 360 × 640); the authentication, the rate limits and CSRF are allauth's, untouched; a wrong address and a wrong
password get the same page.

Both of the owner's complaints are answered — the left side now lives *with* the person, and the form is a real ILE form,
not a SaaS card. Four things are below the bar and are fixed before it ships, none of them a new direction: the stage's
photograph is soft on every HiDPI screen (M1, a `<picture>` the home already has); a revealed password outside the sign-in
keeps the browser's spelling and the keyboard's corrections (M2, three attributes in one place); the sign-up's name field
misses its input purpose (M3, one attribute); and the production `collectstatic` stops on this family's raw entry (M4, the
steward's build fix at the merge — it blocks a deployment, not the preview).

## The owner's two complaints

**1 · «The left side is too static» — answered.** The stage is now a place with depth (the night niche behind the light wall,
the wall's reveal, the floor with four routes converging on the threshold, the warm pool) and it answers every step of the
form, then falls silent:

| The person | The stage (classes logged on the page; the same in Arabic) | Seen |
|---|---|---|
| arrives (from outside the entrance) | `is-arriving`: four lights travel the routes into the threshold, one after another, once (2.4 s) | `states/sheet-arrival-fr-1440.png` |
| clicks «Courriel» | `is-ways`: one pass of light up the four routes; the routes stay lit in their audience accents | `states/sheet-email-focus-fr.png` |
| has typed a valid address (read at the typing pause) | `is-ways is-held`: threshold, pool and the three steps take the gold | `states/states-fr-1440-email-valid.png` |
| clicks the password | `+ is-frame`: the light rises from the threshold up the arch, which holds in gold | `states/sheet-pw-focus-fr.png` |
| submits | the stage's key turns once about its shaft and holds; the primary's own key turns with it | `cast/sheet-cast-fr-1440.png` |
| is refused | the page loads at rest on the still of the kept address (`is-ways is-held`), no arrival | `states/states-fr-1440-after-refusal.png` |

Nothing loops: `document.getAnimations()` is empty at rest, after every pass and on the refused page; the keyboard gets the
states at once (0 animations 40 ms after a Tab, `data-input="key"`); reduced motion shows every end state at once (0
animations); forced colours draw the routes in `CanvasText`; without script the rest picture is whole. The key's turn was
filmed with the POST held 2 s at the network (CDP screencast, the page's own clock): `aria-busy` and the busy face in the
submit's task, `is-engaged` on the stage 13 ms later, the door's key edge-on at ≈ +250 ms, its bit on the other side at
+268…+302 ms, home by ≈ +360 ms, then still until the answer — the turning the owner asked for, never gating the navigation.
It does not distract from the form: every change is the person's own act, 480–600 ms, at the edge of the eye. The one weak
moment is the arrival, which a person who has not acted yet sees as four small sparks (m2).

**2 · «The form is too simple» — answered.** One column on the paper (no floating card), hung at the arch's height; eyebrow
with the registry's key, one title, the invitation; 52 px plates with the label above, the one teal ring with its halo; the
«forgotten password» link at the end of the label's row (after the control in the Tab order); the eye in its 44 px seat,
one name, `aria-pressed`, the caret kept; a flat full-width primary that *holds the key* the loader turns; every unhappy
state composed from live strings — the refusal said once, focused, both fields pointing to it, no red edge, the address
kept and the password emptied, «Erreur — » first in the title; field errors with the doubled garnet edge, the mark and the
words; the 429 on the same layout. Against the V4 comp (`evidence/v54/w2-b/before/login-fr-1440.png`) it is a clear step:
calmer, more exact, and the key ties the form to the stage. It is credible next to the best sign-in pages without
borrowing their look. What keeps the whole surface from feeling finished on a MacBook is the stage's photograph (M1), not
the form.

## Security — an authentication page

- **Authentication, rate limits, CSRF: untouched.** `ACCOUNT_FORMS` gains one key; `accounts.forms.LoginForm` overrides
  `__init__` only (presentation attributes, the password's help beside its label) plus a `bound_field_class` that adds the
  summary's id to `aria-describedby`; the test holds it member by member. `ACCOUNT_RATE_LIMITS` unchanged; the CSRF token
  comes through allauth's own template (`block.super`); `form-action 'self'`; the page is `no-store`.
- **No user enumeration.** Test client against `ile_v5_l7` (its own cache — the server's limits untouched): a wrong password
  for an existing account and an address with no account → 200 and 200, headers equal, bodies identical once the CSRF token
  and the typed address are normalised, fr and ar; the sixth failed attempt says the same sentence for both. The stage's
  still after a refusal depends only on the address's syntax.
- **The 429 reveals nothing.** Reached by asking the reset four times for one address (3/h/key): status 429, «Trop de
  requêtes», the product's one sentence, the way back to the sign-in; no countdown, no limit named; Arabic the same. A
  signed-in person gets the product's error page (test).
- **No credential logged or put in a URL.** Every form is `method="post"`; the server log carries paths only; the audit
  records `auth.login_failed` with no credential, not even the address; `entrance.js` writes classes only — no storage, no
  network, no console, no style.
- **Autocomplete.** Sign-in `email` / `current-password`; sign-up `email` / `new-password` ×2; reset `email`; new password
  `new-password` ×2; second factor `one-time-code`. Two gaps: the sign-up's name (M3) and, outside the sign-in, the revealed
  password's spelling (M2).

## Findings

### Blocking — none

### Major — fixed before it ships

**M1 · The stage's photograph is soft on every HiDPI screen.** `templates/allauth/layouts/entrance.html:68` serves only
`brand/v2/doorway-arch-400.webp` (preloaded at `:47`). At 1440 × 900 its box is 275 × 368 CSS px, so at device scale 2 the
400 px file is stretched over 550 device px (1.4×; 1.8× at the stage's widest, where the arch is 362 px): the statues and
the frieze blur next to the crisp vector arch and key (`dpr/zoom-photo-dpr2.png`). The home now serves the same photograph —
same registration (`static/brand/v5/PROVENANCE.json`) — from 400 to 1200 px in AVIF and WebP (`doorway-arch-960.avif` for
its 474 px box), so going from the home to the login the door visibly loses its focus. The notes' «what is left» 6 waited
for these files: they are on the branch since the design-v5 merge. **Fix:** the home's `<picture class="door-stage__photo">`
sources with a `sizes` that follows the photo box, ≈ 0.87 × `--door-w` (from 64rem `clamp(15.5rem, 22vw, 26rem)`,
`clamp(14.5rem, 20vw, 18rem)` on short desktops, 4.875 / 5.5 / 2.75rem in the band); the preload moved to `imagesrcset` /
`imagesizes` (or dropped for `fetchpriority`) so one file is fetched; check that `_door.css` draws a `picture` as it draws
the span, and re-measure LCP / CLS on the twin.

**M2 · A revealed password outside the sign-in keeps the browser's spelling and the keyboard's corrections.** The sign-up's
two passwords and the new password (`/compte/password/reset/key/…`) are served without `spellcheck="false"` and
`autocapitalize="none"`; the system's show / hide control (`static/js/src/shell.js` §3) turns them into `type="text"`. With
Chrome's enhanced spell check or Edge's Editor, a revealed field's text goes to the vendor's spelling service; on a phone the
keyboard capitalises and auto-corrects it — on the very pages where a person types a new password and reveals it to check it.
The sign-in is protected (`LOGIN_PRESENTATION` sets both), which shows the intent. (Headless Chromium reports
`spellcheck = false` with no spell checker loaded, so this was read from the markup, not observed.) **Fix:** in `shell.js`
§3, the section this family already changes, set `input.spellcheck = false`, `autocapitalize="none"` and
`autocorrect="off"` on each toggle's input when it is wired — every revealable password of the site at once, and without
script there is no reveal — with a test that every `[data-password-toggle]`'s input carries them.

**M3 · The sign-up's «Nom et prénom» has no input purpose** (WCAG 2.2 AA, 1.3.5): `<input type="text" name="full_name" …>`
with no `autocomplete`. It is V4's, but the page is now this family's. **Fix:** `autocomplete="name"` in
`SignupForm.__init__`, which the family already edits, and its test.

**M4 · The production `collectstatic` stops on this family's raw entry** — the implementer's own finding (DL54-59 item 16),
reproduced: the dev settings with `whitenoise.storage.CompressedManifestStaticFilesStorage` into a scratch root →
`SuspiciousFileOperation` on `../../../../static/css/v5/_door.css`, imported by `apps/accounts/static/accounts/entrance.css`.
Nothing a person sees depends on it and the preview is unaffected, but no deployment passes. **Fix (the steward, at the
merge):** the same correction design-v5 owes the console's entry (DL54-44 item 4) — a build-only entry outside `static/`, or
static-namespace imports resolved by `scripts/build_css.mjs` — or the two partials moved beside their importer; then the
command must pass under the production storage.

### Minor — polish

**m1 · From 64rem the niche stops 80 px short of the footer.** The footer's `margin-block-start: 80px` leaves a band of light
wall between the stage (ends at 932 px at 1440 × 900) and the night footer (1012 px): below the fold on the sign-in, at the
end of the sign-up's scroll (`rest/full-fr-1440.png`, `pages/signup-fr-1440.png`). Let the stage meet the footer on the
entrance (or carry its night down), unless that band is meant — then say so in the sheet.

**m2 · The arrival reads as four sparks.** Its beads are ≈ 8 px on 1 px routes that read grey at rest
(`states/arrival-fr-1440-a-02100-floor.png`); a person who has not acted yet may miss it — the owner's «animazioni talmente
sottili da risultare virtualmente assenti». Let each route light up behind its bead (the focus pass already draws
`.varco__way-lit` with `varco-draw`) and fade back as it arrives: same tokens, same 2.4 s, still once.

**m3 · The assurance is French on the it / en / ar sign-in.** It is the locked FAQ quoted as the home quotes it (`lang="fr"`,
LTR in Arabic), so it is consistent with the product; but on the sign-in it is an optional addition, and a French paragraph
under the action of an English or Arabic page reads as a missing translation where trust is meant. Render it only when the
registry holds the page's language (`faq_fallback`), keeping the Privacy Policy link everywhere — or keep it, as the owner's
content call.

**m4 · allauth's reset, new-password and second-factor forms keep their placeholders, and the code its text keyboard.** The
sheet hides them, but assistive technology may still read «Nouveau mot de passe», «Code» a second time. `ACCOUNT_FORMS`
`reset_password` / `reset_password_from_key` (the same setting) without placeholders; `MFA_FORMS["authenticate"]` with
`inputmode="numeric"` — safe for both codes: allauth's recovery codes are 8 digits too (65.19.4) — a second setting, so the
steward's nod.

**m5 · The sign-in's address could say `autocomplete="username"`.** `email` is valid, but password managers and the phones'
suggestion bars key a saved credential on `username` (the usual sign-in guidance), and `email` can offer the person's
contact card instead. Presentation only, in `LOGIN_PRESENTATION`.

## What holds (looked at, nothing to change)

RTL: the page mirrors — stage at the reading edge, eye and key at the plate's and the primary's inline end, the reset link
at the label row's end — while the door, the key, the steps and the routes do not. Phones: the band keeps the action in the
first viewport at 360 × 640 (lower edge ≈ 612 px fr), the frame answers on focus. The same layout carries the sign-up (the
set sticky while the form scrolls), the reset (form, sent, bad key), the new password, the verification (sent with its
session message in the form's column, valid link, expired link), the inactive account, the second factor (the key turns on
its submit) and the re-authentication — fr and ar, 1440 and 390 (the re-authentication in fr at 1440), consistent. From the
skip link's target the Tab order is the invitation's link, the address, the password, its eye, the reset link, the action.
The CTA is flat in every state, the press goes down at once, the label never moves. Ownership: 11 inside, 8 slice, 16
generated, 3 outside (`_varco.css`, `form__entrance.html`, `shell.js` §3 — justified in the notes, for the merge to write
into the manifest). Tests run here: `apps/accounts/tests/test_login_form_w2_b.py` + `tests/frontend/test_429_w2_b.py`, not
in a browser: 21 passed. The login's CSS is 2.5 KB over its ceiling (the notes): for the performance check.

## What I looked at, and the limits

- The real pages on my server, one headless Chromium at a time with its own profile, every series behind the benchmark lock
  (never present), never 8780, 9222 or 9223; no run crashed. The sign-in at rest in four languages (fr, ar at five sizes;
  it, en at 1440 and 390) and full-page; its states, fr and ar at 1440 and 390, under a pointer, from the keyboard, under
  reduced motion, forced colours and with no script, at device scale 2; the submit filmed with the POST held; a refusal, an
  empty submit; ten other entrance pages fr and ar at 1440 and 390, the re-authentication in fr at 1440; the 429 reached for
  real on this server's own cache; the home's door for comparison. Sessions behind a sign-in were minted on `ile_v5_l7` with
  `Client.force_login` and allauth's own `perform_login` for throwaway accounts with unusable passwords — no password used,
  typed or stored.
- Evidence: `C:/tmp/ile_v5_council/evidence/v54/w2-b/review/` (`rest/`, `states/`, `cast/`, `pages/`, `more/`, `stills/`,
  `errors/`, `dpr/`, `home/`; `submit/` and `submit2/` are the first two film attempts — the POST answered at once, then
  the frames blocked by the held navigation — not used); rigs in `C:/tmp/ile_v5_council/.work/w2-b/w2-b-review/`.
- Not verified: no Safari, no Firefox, no real phone, no screen reader, no password manager; no real sign-in (so the release
  on the first console page, W1-D's, was not re-checked); the motion was judged on frames and screencasts, not watched at speed
  on a display.
