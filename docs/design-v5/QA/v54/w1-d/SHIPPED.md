# W1-D shipped — 9 October 2026

**Motion foundation and the definitive signature loader «Lume» — door, rotating key, unlock, light.** Tag
**`v54/w1-d`** (design-v5 `13ce8c4`); the owner's preview on http://127.0.0.1:8780 serves it (v5-live checked out at
the tag, 8780 restarted at 17:14 and verified). Steward's merge, label `w1-d-merge`, under `DESIGN_V5_MERGE_LOCK` from
16:49 (taken when W1-B's merge released it).

## What shipped

- **Reduced motion is a state, not a switch.** `static/css/v5/tokens.css` zeroes every V5 duration under
  `prefers-reduced-motion: reduce` — the key, the door, the light and the staggers included — and `html.rm` is the same
  list for review; the universal `0.01ms !important` rule of `components.css` is gone. Two names keep their value:
  `--motion-wait` (a threshold) and `--motion-reduced` (the one 80 ms opacity an overlay may keep).
- **One gate for script motion.** `static/js/src/motion.js` (`play`, `nextFrame`, `afterPaint`, `tween`, `settled`,
  `reducedMotion()`): the console, the «Ma situation» wizard and «Il portico» ask it, and no other module reads the
  media query or a frame by itself. `static/js/head.js` writes `html[data-input]`, so a change asked from the
  keyboard does not animate.
- **The release** — the second half of the entrance. On the first console page after a successful sign-in the doorway
  of the mark lights from the key's eye and returns to the verbatim mark: once per session, 1.6 s, in the rail's mark
  and, below 1024 px, in the top bar's. It is served, not scripted: `user_logged_in` leaves a flag in the session
  (`accounts.signals`), the console's chrome consumes it once (`{% entrance_release %}`), and the console-only
  generated sheet `v5/_loader-light.css` draws it from the first paint, with or without script. A refused sign-in
  never lights; the mark never mirrors in Arabic; under reduced motion the page shows the still; under forced colours
  neither the room nor the ink is drawn.
- **The busy key** on every form. A submitted `.btn` waits with `aria-busy` and the mark's key turning once in its
  inline-end padding, in the submit's own task, with no shift of the label; a guarded form (`data-single-submit`)
  refuses the second submit with `aria-disabled`, never `disabled`, so the focus stays. **No wait is for ever:** a
  wait is a lease of 10 s (longer for an upload); the one form whose answer is a file says `data-loader="none"` (the
  account's JSON export); a page restored from the cache comes back at rest. A link-styled or icon-only button waits
  without a key (it has no place for one); a control that is not a `.btn` declares nothing.
- **The seat of fetched rows** (the third tier) ships as a primitive and on the board; the Wave-3 families attach it
  to their containers.
- **One state machine**, `static/js/src/loader.js` (1 504 B gzip), imported by `shell.js` on the first submit and
  never before. `templates/components/loader.html` and `busy_key.html`; the board
  `templates/dev/designpreview/specimens/loader.html`.

## The merge

- The branch took design-v5 with W1-B first (`36a3222`; design-v5 was `2a1a672`). Four conflicts, both families kept:
  the decision log (below), the preview's board test (the icon board and the loader board are both linked), one
  regenerated weight in DS 2026 §2, and `dist/main.css` (not resolved by hand: the bundles rebuilt from a clean dist).
- **Numbering.** W1-B's entries reached design-v5 first as DL54-26 … DL54-36, so W1-D's two entries are **DL54-37**
  (the loader as built, with its addenda) and **DL54-38** (every V5 duration at 0 ms), content unchanged. The family's
  notes and reports cite them as DL54-26 / 27 and, before 9 October, DL54-20 / 21 (`ca096a1`; `NOTES.md`, last section).
- Ownership: the twelve paths outside the slice were read in the diff, judged the family's and written into
  `OWNERSHIP_V54.json` under w1-d, as slices wherever another family holds the file (`faa89a2`); two existing slices
  name what was written. `scripts/check_ownership.py w1-d design-v5`: 19 inside, 22 slice, 15 generated — PASS
  (before: 12 outside).
- design-v5 `a3dc6f3` (no-ff; `2a1a672` + `faa89a2`). Bundles rebuilt from a clean `static/js/dist` in both
  worktrees: on design-v5 the two shared chunks take that worktree's names (`27c631f`), byte for byte the same code.
  `scripts/regen_design_inventory.py`: current on design-v5 (one §2 weight rewritten in the pre-merge sync).
  `docs/qa/design/capture.py` on the lane: 43 captures, 842 icons laid out, 0 empty, the focus on the error summary
  after an invalid sign-in — the committed report figure for figure, so it was not re-committed.
- Bytes (gzip −9): `dist/main.css` 43 933 B — under every Wave-1 ceiling of plan §2.6 (home 46 753 of 47 306;
  interior 43 933 of 44 486; login 45 141 of 45 694; dashboard 49 556 of 49 860). 553 B are left on the home and 304 B
  on the dashboard: the next family lands over unless it deletes the legacy rules it supersedes.
- Steward's files (`13ce8c4`): `live_status.json` — the family row, state `v5`, tag `v54/w1-d`; no surface key
  changes (no page type's composition passes with a loader; the pages stay «V4 + fondation»). `CHANGELOG_V54.md` — the
  new entry first.

## Where to see it — http://127.0.0.1:8780

- `/__design-v5/` → «Personas» → «Entrer»: the first page of the console lights the doorway **in the mark at the top
  of the side column** (below 1024 px, the mark of the top bar). It is a detail of 24 px that lasts a second and a
  half: look there as the page arrives. It plays once per session — «Sortir», then «Entrer», plays it again.
- `/__design-v5/specimens/loader/` — the board, frame by frame: the engage (the key turns once and holds), the
  release, the busy key on the button variants, the seat, and the reduced-motion stills.
- `/__design-v5/index/` — «Stati senza credenziali»: «L’ingresso, dopo «Entrer»» no longer says «in arrivo»; the
  family is listed as passed, with its review (`/__design-v5/decisioni/w1-d/REVIEW.md`).
- `/fr/compte/login/` and `/ar/compte/login/` — any address and a wrong password: «Connexion» waits with the key,
  the error page arrives at rest. `/fr/orientation/` («Commencer») and `/fr/contact/formulaire/` («Envoyer le
  message») — the same key on their buttons.
- Inside a persona's session a form's submit is answered 403 by design (the preview's sessions are read-only): the
  key turns, then the refusal arrives.

Checked on 8780 after the restart, by request only (no browser on the owner's server): `/fr/`, `/ar/`, `/it/`, `/en/`,
`/__design-v5/`, the index, the two boards, the review, the two logins, the sign-up, the password reset, the
orientation and the contact form answer 200; the strip names `v54/w1-d` · `13ce8c4`; the bundles and the two chunks
are served with the built sizes. One round trip through the preview's own persona switch (qa-doc-person, no password):
the first console page answers 200 with the release on its two marks, the second with none, the Arabic console, the
profile (its export form says `data-loader="none"`), `/documents/` and the communications answer 200; then «Sortir».
The server log holds no traceback and no 500; no database connection left open. That round trip left one sign-in and
one sign-out of that persona in the audit trail of `ile_v5`.

## Tests (lane 7, `test_ile_v5_l7`; every run completed, none crashed)

On the branch with design-v5 merged in (`faa89a2`):

- Not in a browser — **1 164 passed, 0 failed, 0 skipped**: the loader's rules and its Django-client tests, the
  reduced-motion flag's parity, the script motion gate, both bundle-currency files, the design documents, the V5 and V4
  tokens, the preview (its browser tests apart), the ownership and inventory tools, `apps/accounts`, `tests/security`.
- In a browser (Chromium, one at a time) — **37 passed, 0 skipped**: `tests/frontend/test_loader_w1_d.py` 22 ·
  `tests/frontend/test_reduced_motion_w1_d.py` 7 · `apps/portal/tests/test_browser.py` 8.
- On design-v5 after the merge and the rebuild: 663 passed (the same static files, bundle currency included).
- The full suite is the integration checkpoint's (V5.5); it was not run here.

## Not done

- **The engage on the login** — the key turning on the stage at 160 px, where the signature becomes legible — is
  W2-B's wiring on this primitive. Until then the sign-in shows the busy key on its button and the release on arrival.
- **At the served size the release is quiet**: a change of about 6 × 8 px inside a 24 px mark on a 1× desktop
  (review m1). Under reduced motion it is the verbatim mark, not a lit still (review m4: the Creative Director's to
  take or leave).
- **The seat of fetched rows has no product container yet** (no region of the product fetches asynchronously today).
- **Other families' work, named in `NOTES.md` «Handed to»:** V4's busy rule repaints every waiting button as the
  primary, and the icon button's busy face (W1-C); the dashboard's two V4 entrances at load, `rail-draw` and
  `strip-fill` (W3-B, W3-D); the home hero's looping `route-current` (W2-D); the account menu's logout, which is not a
  button of the system and shows no wait (W2-A); the index's sentence still says «nella colonna di sinistra» and could
  name the top bar's mark (W1-P); on the Arabic login at 390 px the password's placeholder runs under the show / hide
  control, as before this family (W2-B); `data-loader="none"` must survive a rewrite of the profile page (W3-F2).
- **Not run:** Firefox and WebKit; a real back/forward cache beyond one public page; a person watching the motion at
  speed; the performance PASS on 8782 (the family's check measured no regression on the lane).
- **Not this family's, still open on design-v5:** six cases of `test_state_chips_carry_a_register` fail at the tag,
  on four of the preview's own templates (`_family.html`, `_row.html`, `_strip.html`, `index.html`). The test, the
  templates and the chips registry are byte-identical at `2a1a672` and at the tag: this merge did not cause them.
