# V5.20 strict test-change audit (label `v520-audit`)

30 October 2026. **Read-only.** Nothing in the repository or the worktree was changed. The private sentinel table was not opened. No phone number appears anywhere in this file.

- **Tree:** design-v5 worktree `C:/tmp/ile_wt/design-v5`.
- **Range:** `238dc1c` (tag `v515/d`, 29 Oct 16:47) to `e2098dd` (tag `v518/green`, 30 Oct 03:40). That is 49 commits.
- **Scope:**
  - every changed test file: 53 files, +957 / −190 lines, `tests/conftest.py` included;
  - the ratchet and budget constants;
  - the allow and except lists;
  - pytest markers, skips, xfails, waits and timeouts.
- **Rule** (owner, V5.20, 29 Oct 23:47): a test may change only if all four of these hold:
  1. the old expectation conflicts with an explicitly approved owner or product decision;
  2. the new behaviour is implemented on purpose;
  3. the test protects the same invariant or a stronger one;
  4. the reason is cited.

## 1. Verdict

| | Count |
|---|---|
| Changed assertions and guards judged | 80 |
| **OK** (all four conditions hold) | **67** |
| **VIOLATION of the test rule** | **12** (V1–V12) |
| Breaks decision B, not the test rule | 1 (V13) |

**Effect on the V5.20 gate** («FAILURES = 0 / BLOCKING LINT = 0 / UNEXPECTED SKIPS = 0 / P0/P1 = 0»):

- **P1, gate items:**
  - V1 and V2: the shared stylesheet is over budget and its ratchet was loosened.
  - V3 and V4: the guards accept an animation that stays applied after it ends, a class V5.20 calls a release blocker.
  - V5: the Arabic brand jump when the phone menu opens was turned into expected behaviour.
  - V11: four unexpected skips.
- **P2:** V6–V10 and V12.
- **Push blocker:** V13. The confidential-material guard stays red with the private table configured.

**Unchanged in the range** (checked by diff):

- `pyproject.toml` (the pytest and ruff configuration);
- `.github/workflows`, `requirements/`, `package.json`;
- the `KNOWN_*` and `RUNTIME_PROPERTIES` lists. `KNOWN_OVERFLOW` is still empty.

**Also verified:**

- No `# noqa` was added.
- No test file was deleted, and no test was removed without its replacement.
- No xfail was added.
- No timeout was increased.

**Skips (8):**

- 7 should run with a fixture: the 3 intake cases and the 4 contact-channel `/faq/` cases.
- 1 is genuinely environment-bound: the private table.

**Xfails (2):** both are recorded debts, older than the range (§6).

## 2. How the rule was applied

**What counts as an approved decision.** These count:

- the owner's directives;
- decisions those directives authorise, if they were **recorded before the test changed**. Examples:
  - the Director's DECISIONS.md, last written 28 Oct 20:23;
  - a DL entry older than the change;
  - the V5.18 audits' findings (29 Oct 16:45), which came before the fixes.

A ruling made during the green suite to close a guard that was already failing does not meet condition 1 on its own. This applies to DL54-178 and to DL54-179 item 6.

**Timeline**

| When | What |
|---|---|
| 28 Oct 16:07 | V5.15, the creative override (DECISIONS §15) |
| 28 Oct 20:23 | DECISIONS.md last written (§8, §9, §15, §16) |
| 29 Oct 15:53 | V5.18 |
| 29 Oct 16:45 | V5.18 quality audit (P-1 … P-9) and the integrated findings (B1–B3, P7–P12, T1–T3) |
| 29 Oct 16:47 | base `238dc1c`: main.css 33 448 B gzip -9, ceiling `<= 33_448` (exactly at it) |
| 29 Oct 18:13–20:30 | V5.18 lanes A–D: fixes and T3 test updates |
| 29 Oct 18:29 | V5.19 (contact channels; §15 «Do not weaken existing tests») |
| 29 Oct 20:49 | steward `5f92e4d` (the T3 test resolutions) |
| 29 Oct 20:52 / 20:53 | lane K `9dc75f6` raises the main.css ceiling to 33 576; `5993190` raises it to 33 600 |
| 29 Oct 23:15–23:27 | groups N and C |
| **29 Oct 23:47** | **V5.20** |
| 30 Oct 00:07 | group P `5903f0c`: FORMWORK_CORNERS, ADMITTED_RAISED, the RTL mark assertion |
| 30 Oct 00:53 | steward `2f95909`: ceiling «re-seated» at 33 530 |
| 30 Oct 02:52 | steward `a071a9b`: the WhatsApp helper |
| 30 Oct 03:40 | `e2098dd` (`v518/green`) |

**Correction to the brief.** «Inconsistent corners» is not in V5.12 §12, which is about the preview labels. The owner's own words on corners are:

- V5.1 §85: «corner consistency» and «drop shadow density», listed among the high-end details;
- V5.1 §11: «enormi border radius senza sistema», listed as a generic-AI symptom;
- V5.2 §28: «DESIGN TOKENS FIRST … radius; shadow».

The team's rule that implements them is plan §1.3 (DL54-14). It is written into `static/css/v5/tokens.css:106-112`: «at most three distinct radii on a screen at rest». The finding on DL54-178 (V6) stands on these.

## 3. Violations

### V1. The main.css ceiling was raised in `tests/frontend/test_forms_v515_b.py:177` and `:278` (P1)

**What changed.** Both guards were `<= 33_448`. They became:

1. `33_576` (lane K, `9dc75f6`, 29 Oct 20:52);
2. `33_600` (`5993190`, 20:53, citing «lane A's V5.15 exception»);
3. `33_530` (steward `2f95909`, 30 Oct 00:53, «re-seated at its measure»).

That is 82 B gzip -9 above the base ceiling. The measure at `e2098dd` is 33 530 B, checked here with `gzip.compress(…, 9)`, so the guards have 0 B of headroom.

**Rules broken: conditions 1 and 3.**

- No owner decision approved a larger shared bundle. V5.19, the reason the lane gave, orders the channels, not a budget, and says «Do not weaken existing tests» (§15).
- V5.8 (owner), with the orchestrator's definitive ruling of 12 Oct: «No merge may raise either one above its weight … A family that needs a new shared rule pays for it with deletions … Nobody records a shared ceiling higher.»
- V5.20 lists «shared stylesheet over budget» as a release blocker: «prefer deduplication, dead-rule removal and route-specific loading over simply raising the limit».
- DL54-176 item 2 itself records the change as «a ratchet loosened».
- The new comment cites «V5.8: a shared bundle ratchets down», which describes the opposite of what the change does. That also fails condition 4 in substance.

**Product fix (preferred).** Remove at least 82 B gzip from `static/css/dist/main.css` with no visible change. Options:

- Names of the legacy shim that nothing reads (`static/css/_legacy-tokens.css`, which is in main.css). There is precedent: v512-a-fix-w1 and v512-a-w2 paid for main.css this way, and `MAX_SHIM_TOKENS` was lowered in the same commit.
- Shared selectors with no producer, proved by coverage over every route and state. Group N already used this method and took the bundle from 33 455 to 33 406 B.
- Duplicate rules.
- Anything only one route draws moves to that route's page sheet. The contact page's plates are already page-only (`_canali.css`). The footer and phone-sheet channel rules must stay shared, so they are paid for by deletions.

**Exact restoration.** Set both lines back to:

```python
assert gz(STATIC / "css" / "dist" / "main.css") <= 33_448
```

Use the comment «V5.8 / V5.20: the shared bundle never rises; lane K's channels are paid by deletions». In the same commit as the cut, lower the ceiling to the new measure.

### V2. Lane A's main.css ceilings were kept slack in `tests/frontend/test_motion_v512_a_w2.py:113` and `tests/frontend/test_lume_v515_a.py:243` (P1)

**What changed.** The lines were not edited in the range. But DL54-179 item 6 (30 Oct, in the range) decided to keep `<= 33_600` as «that exception's own bound».

**Rule broken.** V5.8 rule 1 says «Savings are locked in: after a merge, the merged weight is the new ceiling». These two ceilings sat 152 B above 33 448. Lane K used exactly that slack to justify its raise («the ceiling is lane A's V5.15 exception»). A slack ceiling is a loosened ratchet under V5.20.

Lane A's exception itself is not in question: DL54-170 allowed 31 414 → at most 33 600 B for the veil, the global loader the owner ordered in V5.15 §8–§10. The problem is that its bound was never re-seated at the measure.

**Restoration.** After the V1 cut, set all four main.css guards to the one measured value (≤ 33 448):

- `test_forms_v515_b` ×2;
- `test_motion_v512_a_w2:113`;
- `test_lume_v515_a:243`.

Ideally all four read one constant, for example `MAIN_CSS_GZIP_CEILING` in a shared test helper, so they cannot drift apart again. Cite V5.8 and V5.20.

### V3. «moving» skips a finished `c-rise` in `tests/frontend/test_dashboard_browser_w3_b.py:66-76` (used at :109 and :251) (P1)

**What changed.** `moving` used to list every animation in the workspace. Now it leaves out `c-rise` when `playState === 'finished'`. This came from lane B, `24b3bbb`, 29 Oct 19:01, with the note «its `both` fill keeps a finished rise in getAnimations()».

**Rules broken: conditions 1 and 3, and «convert real regressions into expected behaviour».**

- A finished animation that is still listed is the class V5.20 calls a release blocker: «animation remaining applied after completion … ensure completed animations clean up their final transient state».
- The product has been fixed: `c-rise … backwards` in `apps/portal/static/portal/v5/_motion.css:181` and `static/css/v5/_conto-console.css:36` (lane A `a9ad225`, `cb0b35d`). So the exclusion is now dead code. Its only effect is to let a `both` fill come back unseen.
- Lane A's own comment in the same file (:46-48) already says «it fills backwards only, so an ended rise is no longer listed».

**Exact restoration.** Put back the expression from before the change:

```python
MOVING_JS = """(ws) => document.getAnimations().filter((a) => a.effect && a.effect.target && ws.contains(a.effect.target))
  .map((a) => a.animationName || a.transitionProperty || 'waapi')"""
```

Delete the comment at :66-70. The `c-rise` await in SETTLE_JS (:53-54) is a wait for a finite animation, so it stays (O57). The restored guard should pass at HEAD.

### V4. «Nothing loops» counts only running time-based animations in `apps/pages/tests/test_browser.py:552-560` (P1)

**What changed.** The check was `document.getAnimations().length == 0`. Now it lists only infinite animations and time-based animations that are still `running`. Lanes A (`a9ad225`) and C (`b2ebd35`) both made this change, and the steward kept lane C's form (`5f92e4d`).

**Rule broken: condition 3.**

- Letting lane A's scroll-driven reveals stay is justified: they are ViewTimeline animations, and V5.15 §6 orders «section reveals».
- The filter also lets through any time-based animation that has *finished* and stays applied by its fill. That is the V5.20 release-blocker class.

**Restoration.** This is the strongest form that still fits V5.15 §6:

```js
const timed = !a.timeline || a.timeline instanceof DocumentTimeline;
const forever = a.effect && a.effect.getComputedTiming().iterations === Infinity;
return forever || timed;
```

Any time-based animation still listed fails, whether it is running, paused or finished with a fill. Only finite scroll-driven reveals pass.

If this fails at HEAD, fix the code, not the test: the animation fills `backwards`, as the V5.18 rule says («backwards, never both»; see §7 for the fills still left in code).

### V5. The sheet's mark may move in Arabic: `tests/frontend/test_browser_w2_c2.py:128-133` (P1)

**What changed.** The check was `assert rows["head"] == rows["bar"]`. Now it compares the start edge and the vertical edges, and checks that the mark does not move only `if not rows["rtl"]`. Group P made this change (`5903f0c`, 30 Oct 00:07), after V5.20.

**The LTR part is OK** and is counted as O50. V5.13 Q1 has the home's bar draw the mark alone.

**The RTL branch is not justified.**

- In Arabic, opening the sheet moves the brand mark about 183 px. Group P observed this itself and DL54-179 item 10 left it «for lane A».
- V5.18 §1 orders «all RTL alignment issues in the same family» fixed.
- So this turns a visible regression into expected behaviour.

**Cause.** `static/css/v5/chrome.css:37-45` sets the whole lock-up, mark and words, to `direction: ltr`. In the sheet's head the lock-up grows from the right edge, so the mark sits at the isolate's left end.

**Product fix** (the Director's call; the brand rule «never mirror the mark» binds it). The sheet's head must keep the mark where the bar draws it. Two ways:

- The sheet's head draws the mark alone on the home, as the bar does. Q1's «one name on the screen» then holds inside the sheet too, and the original `head == bar` assertion comes back verbatim.
- Or the Arabic sheet head is laid out so that its mark lands on the bar's mark.

**Restoration.** Replace :130-132 with `assert rows["headMark"] == rows["barMark"], rows` in both directions, and delete the Arabic sentence of the comment at :115-116.

### V6. The formwork's own corner set (FORMWORK_CORNERS), DL54-178 item 1, in `tests/frontend/test_content_pages_browser_w3_f2.py:58-66`, `:81`, `:318-322` (P2)

**What changed.** Corners inside `.formwork` no longer count toward the page's three-corner rule (§1.3). Instead they need only belong to {12, 8, 6, 4, 999, 6.4, 1} px. Group P made this change (`5903f0c`), after V5.20.

**Measured** (group P's `probe_formwork.json`). The formwork alone draws 5 to 7 distinct radii on a screen:

| Radius | Elements |
|---|---|
| 12 | grid, panel, steps head |
| 6 | fields, consent tick, step tiles |
| 8 | consent box |
| 4 | the action |
| 6.4 | the glyph tile |
| 999 | the «optional» pill |
| 1 | the 2 px step bar |

tokens.css says «at most three distinct radii on a screen at rest». Two of the values are not tokens at all: 6.4 (`_glyph.css:34`, `calc(var(--gt) * 0.2)`) and 1 px (`_steps.css:32` and `:125`). `_formwork.css:115` also writes a literal `3px`. And the formwork overrides the token roles: tokens.css gives fields `sm`, but `_formwork.css:28` sets `--field-radius: var(--radius-md)`.

**Rules broken: conditions 1 and 3.**

- Condition 1: no owner decision approved more radii.
  - V5.15 §15 (premium forms) does not mention corners.
  - The owner asks for «corner consistency» (V5.1 §85).
  - DL54-173 (29 Oct) left this failing guard «the Director's to rule». The ruling, DL54-178, was made during the green suite to close it.
- Condition 3: a formwork page can now show up to 9 radius values.

**Product fix (preferred).** Put the formwork on the corner scale so that a formwork screen holds at most three values together with the targa's 6. This is not a redesign: no element moves more than 4 px. One possible mapping, for the Director to decide:

- controls on `--radius-md`: the fields already are; the action goes 4 → 6; the glyph tile's 0.2 × side becomes `--radius-md`;
- containers on `--radius-xl`: the consent box goes 8 → 12;
- the pill and the 2 px step bar on `--radius-full` (a 2 px bar renders the same);
- the literal 3 px moves onto the scale.

If the formwork's own set is to stay, it needs an explicit owner approval cited in the test. That is what V5.20 condition 1 requires; a Director's ruling made during the green suite does not meet it.

**Restoration.**

- PROBE line 81 goes back to `if (drawn && v !== '0px') radii.add(v);`.
- The FORMWORK_CORNERS check (:321-322) goes.
- The §1.3 three-corner rule (:316-317) applies to the whole `<main>` again.
- Keep the new presence check («no formwork drawn» on FORMWORK_PAGES) through a separate flag, for example `out.formwork = !!main.querySelector('.formwork')`.

### V7. Eight surfaces admitted by name with any shadow (V515_RAISED) in `tests/frontend/test_content_pages_browser_w3_f2.py:38-56`, `:83` (P2)

**What changed.** Eight selectors are exempt from «no shadow at rest», whatever shadow they carry. Lane C made this change (`b2ebd35`, 29 Oct 18:13, «T3»).

**Condition 1 holds for shadows.** V5.15 §18 explicitly asks for «shadow hierarchy … layered surfaces».

**Condition 3 does not hold.**

- An admitted element may now carry any shadow. A 200 px blur would pass.
- Two selectors go beyond what the decision covers: `.foto__img` is admitted on every content page, and `.glyph-tile` anywhere in `<main>`.
- Four admitted surfaces draw shadows outside the token hierarchy:
  - the head photograph's drop (`_fronte.css:517`, and the same value again at `:1118`);
  - the current step tile's glow (`_steps.css:73`, `:123`);
  - the glyph tile's drop (`_glyph.css:36`).

**Fix: the strongest invariant** (V5.15 §18 together with V5.20's token rule) is «a shadow at rest only from the token hierarchy, and only on the named surfaces».

- Map each admitted selector to the shadow it may draw. Read the allowed values from the tokens: resolve `--shadow-1…4`, `--shadow-door` and `--passe-partout` on a probe element, as `test_browser_chips_w1_c`'s SHADOW_JS already does.
- Inset hairlines may only be `inset 0 0 0 1px` plus a line token.
- Any other value fails.
- Scope the selectors to the decision, for example `.formwork .glyph-tile`.

On the product side, the four bespoke shadows become tokens of the hierarchy with the same values, so nothing changes visually; the bytes they add to main.css are paid for by deletions (V1). Or they reuse an existing level.

### V8. Two page-head surfaces admitted by name with any raised shadow (ADMITTED_RAISED), DL54-178 item 2, in `tests/frontend/test_orientation_browser_w3_f1.py:36-50`, `:65`, `:126` (P2)

**What changed.** The head photograph's passe-partout and the fraud page's notice panel are exempt from SH-8, «no raised shadow at rest». Group P made this change (`5903f0c`), after V5.20.

**Same analysis as V7.**

- Condition 1 holds: V5.15 §18, and lane C's DL54-172, recorded before.
- Condition 3 does not: the exemption puts no bound on the value.
  - The passe-partout's measured drop (two layers, the second `0 28px 56px -24px` at 42 %) is a literal in `_fronte.css`, outside the hierarchy.
  - The fraud notice uses `--shadow-3` (`_fronte.css:1261-1263`), which is in the hierarchy.

**Answer to the brief's question.** A named exception is not the strongest invariant. The rule should become «shadows at rest only from the token hierarchy», with the named surfaces as the only places a raised level may appear and at most one per first screen.

**Fix.**

- Pin the notice to `--shadow-3` (plus its inset hairline).
- Pin the passe-partout to a hierarchy token that holds today's value. The two literal copies at `_fronte.css:517` and `:1118` are also a duplicate to remove.
- Every other raised shadow still fails.

### V9. Any chip counts as the pill in `tests/frontend/test_dashboard_browser_w3_b.py:99-101` (P2)

**What changed.** GATE_JS now counts every `.chip` as `full`, whatever its radius or shape. Lane B made this change (`24b3bbb`, 19:01) for the case's step chip, which wrapped on a phone.

**Rules broken: conditions 1 and 3, and converting a regression.**

- The wrap was the defect. Lane D fixed it in code 86 minutes later (`72dbf14`, 20:27): the chip keeps «Étape 1 sur 7» on one line, with the step's title beside it. `test_terminology_v512_d` pins that.
- So the exemption is now dead tolerance. It would hide a chip whose radius is off the scale, or a chip that wraps again.

**Exact restoration.** Put back the line from before the change, and delete the comment at :99-100:

```js
if (v && v !== '0px') radii.add(parseFloat(v) >= r.height / 2 - 0.5 || parseFloat(v) >= 100 ? 'full' : v);
```

### V10. The WhatsApp URL is excluded in any attribute in `tests/frontend/test_layout.py:30-32` (P2)

**What changed.** The URL is taken out of the list of external URLs whatever attribute it appears in, `src`, `content` and `action` included. Lane K made this change (`9dc75f6`). The URL is written as a literal.

**Rule broken: condition 3.**

- It is weaker than the owner's order (V5.19 §7: a link the visitor follows).
- It is weaker than the rule every other guard got from `tests/conftest.py::whatsapp_link_set_aside`, which sets aside only an `<a href>` to exactly that URL.
- Here, an `<img src>`, `<form action>` or `<meta content>` to the same URL would pass.
- The literal also puts the number in a test file (V13).

**Exact restoration:**

```python
from tests.conftest import whatsapp_link_set_aside


def _external_urls(html: str) -> list[str]:
    urls = re.findall(r'(?:src|href|content|action)="(https?://[^"]+)"', whatsapp_link_set_aside(html))
    return [u for u in urls if "testserver" not in u and "localhost" not in u]
```

### V11. A conditional skip on any status other than 200 in `apps/pages/tests/test_contact_channels_v519.py:150-153` (P1, gate)

**What changed.** A new test skips whenever the page does not answer 200. Lane K added it (`9dc75f6`). In the CI-style run it skips `/faq/` in all four languages: 4 skips.

**Rule broken:** «skip tests unless the feature is genuinely unavailable in that environment».

- The FAQ can be opened with existing fixtures:
  - `phase3_open` (tests/conftest.py, already re-exported by `apps/pages/tests/conftest.py`);
  - the locked FAQ seeds, `faq.seeds.seed_locked_faq_items()`, as `faq_seeded` in `apps/faq/tests/test_views.py` uses them.
- The same condition would also skip a 500 on `/`, `/contact/`, `/le-projet/` or `/agami/`.
- These skips are the only unexpected ones in the run, so they alone put UNEXPECTED SKIPS above 0.

**Fix.** The test takes `phase3_open` and seeds the locked FAQ items. Then `assert response.status_code == 200, (lang, path)` replaces the skip.

### V12. The account trail no longer names two pages: `tests/frontend/test_service_pages_w3_f2.py:261` and `:266` (P2)

**What changed.** Group N moved the test onto the console frame (`921a895`). In doing so, the trail's current crumb for «Supprimer mon compte» and for «Se déconnecter» became «Mon compte».

**The frame change itself is approved and stronger** (O25).

**These two rows are not.**

- On those pages, the breadcrumb's last item says «Mon compte» with `aria-current="page"`, and the console bar's title, which is drawn from it, says the same. The page is in fact the deletion request or the sign-out.
- The contract in `templates/components/breadcrumbs.html` says «the last item is the current page».
- No decision chose this. DECISIONS «Lane B» acceptance 6 says only «`/fr/compte/*` renders inside the console with the rail».
- Condition 3 fails: the old guard held «the trail names the page».

**Product fix.** In `apps/accounts/shell.py::_page_label` (:73-83), return «Supprimer mon compte» for `accounts:delete_request` and «Se déconnecter» for `account_logout`. Both msgids are already in the it, en and ar catalogues, so no new string and no machine translation are needed. `console_context` then draws «Espace réservé › Mon compte › <the page>».

**Exact restoration.** Set the trail of rows :261 and :266 back to «Supprimer mon compte» and «Se déconnecter», as at `238dc1c`.

### V13. Decision B: test files that write the WhatsApp number (not the test rule; push blocker)

**Files at `e2098dd`** that hold the number in any form, with the count of occurrences:

| File | Occurrences |
|---|---|
| `apps/pages/tests/test_contact_channels_v519.py` | 12 |
| `apps/pages/tests/test_institutional.py` | 2 |
| `tests/frontend/test_browser_contact_channels_v519.py` | 1 |
| `tests/frontend/test_layout.py` | 1 |

With the private table configured, `tests/security/test_confidential_material.py` fails on the first of these and on four non-test files (DL54-179 item 8). The owner has not answered A or B, so B applies: no copy of the number in the repository.

**Fix, keeping every invariant as strong as it is now.**

- **Read the expected values from the canonical source.** The tests take them from `core.contact.public_channels()`, with a fictional number written into SiteSettings by a fixture, from a range reserved for fiction. They still assert exactly:
  - the format;
  - the wa.me shape (`https://wa.me/\d+`);
  - the accessible names, built from the label;
  - the Arabic isolate order;
  - one link per surface;
  - that a blank setting withdraws its channel.
- **Use generic shapes for the template check.** `test_no_template_writes_a_number` checks `tel:\+?\d`, `wa\.me/\d` and any run of 8 or more digits, instead of the owner's digits.
- **Make the settings check environment-driven.** `test_the_settings_hold_the_confirmed_numbers`:
  - asserts that the default holds no WhatsApp number;
  - checks that the configured value is the owner's where the environment provides it, and skips with its reason printed elsewhere. That skip is genuinely environment-bound, like the private-table test. It also keeps V5.19 §15's «URL exactly …» wherever the value exists.
- **Exercise the helper in CI.** Set the same fixture number for the twelve guards O01–O12. Under B, the CI database has no WhatsApp number, so `whatsapp_link_set_aside` would otherwise do nothing there and its «link only» rule would never be tested.

## 4. The questions in the brief

1. **The main.css ceilings:** V1 and V2. Every ceiling (`test_forms_v515_b` ×2, `test_motion_v512_a_w2:113`, `test_lume_v515_a:243`) goes to the measure after the cut, at most 33 448 B.
2. **DL54-177 (the o14 tick): OK (O64).**
   - The check rule (ICON_SEMANTIC_MAP §2 [RT]) reserves `check` for «the person's own interface acts (a ticked box, a chosen OptionCard, a selected filter chip …), never … any state the platform produces». The active language in the language menu is the person's own selection among options (`aria-current="true"`), the same act as a selected filter chip.
   - The admission is pinned: `header.html` may draw `check` once, and only inside `{% if l.active %}`.
   - The product decision came first: lane A's popover (`cb252091`, 28 Oct; DL54-171), and DL54-173 (29 Oct) had already limited the receipt's check test to `<main>` «because lane A's language popover ticks the current language».
   - Documentation follow-up: the [RT] rule's wording should name the language menu, as `icons.CHECK_BEARING` now does.
3. **DL54-178:**
   - The corners are **V6**. No owner approval exists, and the set breaks tokens.css's three-radii rule.
   - The two head shadows are **V8**, and the eight w3-f2 surfaces are **V7**. A named exception is not the strongest invariant. The rule should become «shadows at rest only from the token hierarchy, on named surfaces».
4. **Timeouts and waits:** none was increased.
   - Chips: a fixed 300 ms became a condition (no animation left).
   - The w1-c FAQ mark: a new condition wait.
   - The dashboard's `_settle`: a new condition wait on the arrival veil with a 5 s cap. That is a failure bound, not a sleep; `test_lume_v515_a` guards the veil's own duration.
   - The rewritten sign-in test: 900 ms became 700 + 100 ms. Those are fixed waits, but they were not increased.
   - **Debt:** the new `page.wait_for_timeout(500)` in `test_browser_contact_channels_v519.py:74` should wait for the sheet's animations to end instead.
5. **New skips and xfails:**
   - one new conditional skip (V11);
   - `importorskip` and «Chromium not available» in the new browser fixture: the standard pattern, genuinely environment-bound;
   - no new xfail.
6. **Admit, allow, exclude and except lists:**
   - violations: V7, V8, V6, V3, V9, V10;
   - OK: the helper (O01) and `tests/compliance` (O12), `ARABIC_LATIN_ALLOWED` + «WhatsApp» (O17), the o14 map (O63, O64), the journey's `_compose.css` modifier (O62), the overlays' self-hidden list, now exact (O58), the RTL sweep's exact set of 404s (O44), the ownership ids (O67);
   - the veil exclusion in RADII_JS is OK with a note (O59).
7. **The WhatsApp helper (`a071a9b`): OK (O01).**
   - It sets aside only an `<a href>` to exactly the URL from `core.contact`, so it holds no literal and fits decision B.
   - Two strengthenings are left: a unit test of its negative cases (`<img src>`, `<form action>`, `<meta content>`, `href="…?text=…"`, another wa.me number) using the fixture number; and `\bhref` also matches `data-href` (a nit).
8. **The other areas:**
   - empty state: O20–O23, O37;
   - account frame: O25, with V12 for two trail rows;
   - the Academy row: O31, O32, O35;
   - rail counts: O33, O34;
   - legal links: O38, O40, O41;
   - route floors: O43, O44. Both are tight: 23 ungated routes and 56 distinct paths, counted here.

## 5. The 67 OK changes

In the Basis column, «V5.x» is the owner's directive; «DECISIONS §n» is the Director's document (28 Oct, before the range).

| ID | Where (HEAD) | Change | Basis (recorded before) | Same / stronger |
|---|---|---|---|---|
| O01 | `tests/conftest.py:191` | `whatsapp_link_set_aside`: each `<a href>` to exactly `core.contact`'s URL set aside | V5.19 §5–§7 (the footer and the sheet draw the link); DL54-176 | any other external URL, and the same URL as src, srcset, content or action, still fail |
| O02 | `apps/ecosystem/tests/test_compliance.py:52` | the helper applied | as O01 | the assertion is unchanged |
| O03 | `apps/enquiries/tests/test_compliance.py:56` | idem | as O01 | idem |
| O04 | `apps/faq/tests/test_views.py:223` (compliance scan) | idem | as O01 | idem |
| O05 | `apps/forum/tests/test_forum_page.py:239` | idem | as O01 | idem |
| O06 | `apps/glossary/tests/test_views.py:223` | idem | as O01 | idem |
| O07 | `apps/living/tests/test_compliance.py:66` | idem (salute.gov.it is still the only other URL) | as O01 | idem |
| O08 | `apps/news/tests/test_compliance.py:60` | idem (normattiva is still the only other URL) | as O01 | idem |
| O09 | `apps/orientation/tests/test_compliance.py:131` | idem | as O01 | idem |
| O10 | `apps/pages/tests/test_home.py:103` | idem | as O01 | idem |
| O11 | `apps/pathways/tests/test_compliance.py:91` | idem | as O01 | idem |
| O12 | `tests/compliance/test_public_pages.py:76-86` | the WhatsApp URL admitted only inside an `<a>` | V5.19 §7; DL54-176 item 7 | scripts, styles, fonts and images from anywhere still fail |
| O13 | `apps/pages/tests/test_institutional.py:172-176` | «no tel:, no number» became «exactly the owner's two channels, and no other number» | V5.19 §5, §11, §15 | an exact set (the number literals: V13) |
| O14 | `apps/pages/tests/test_seo.py:54-56` | Organization `telephone` is the Numero Verde; `contactPoint` added to the list of absent keys | V5.19 §13 («no new schema type») | exact value; one more absence asserted |
| O15 | `tests/frontend/test_icons.py:91` | 125 → 126 symbols (`message-circle`) | V5.19 §6, §10 | exact count |
| O16 | `tests/frontend/test_interior_w3_f1.py:392` | `_canali.css` in the contact page's sheet list | V5.19 §11 (route-specific CSS) | exact list |
| O17 | `tests/i18n/test_ui_translations.py:122-130` | «WhatsApp» allowed in Latin script in the Arabic chrome | V5.19 §6, §8, §10 (the channel's brand name, WCAG 2.5.3) | one proper noun added |
| O18 | `apps/pages/tests/test_contact_channels_v519.py` (new; :152-153 excepted, which is V11) | V5.19 §15's tests | V5.19 §15 | new guards (the literals: V13) |
| O19 | `tests/frontend/test_browser_contact_channels_v519.py` (new) | 44 px targets, one line, the Arabic order | V5.19 §12, §9 | new guards (the 500 ms sleep is debt; the literal: V13) |
| O20 | `apps/faq/tests/test_views.py:136-138` | `class="empty-state"` became the component's full opening tag, `role="status"` included | V5.15 §7 / DECISIONS §15 lane B (`9211d5fc`, before the range) | stronger |
| O21 | `apps/glossary/tests/test_views.py:146-148` | idem | idem | stronger |
| O22 | `apps/forum/tests/test_forum_registration.py:194-196` | idem | idem | stronger |
| O23 | `apps/portal/tests/test_views.py:147, :218` | `empty-state empty-state--tile` | idem | same (exact attribute) |
| O24 | `apps/portal/tests/test_views.py:346-350` | non-French dashboards: no locked French head; the translated H1 instead | V5.18 §7 + V5.13 Q3; audit P-3 (16:45, before `3d16ead`) | an exact H1 and an absence (no fallback left to mark) |
| O25 | `tests/frontend/test_service_pages_w3_f2.py:270-285` | the account pages in the console frame; no public frame; the H1 is the page's words | DECISIONS «Lane B» acceptance 6 (V5.12 W2) | stronger (two trail rows: V12) |
| O26 | `tests/frontend/test_service_pages_w3_f2.py:436-461` | «Ma situation»: the CLDR `<select autocomplete="country">`, one control | DECISIONS §5.7 (`751be04c`) | stronger |
| O27 | `tests/frontend/test_login_invitation_w4_d.py:24-27` | the invitation needles follow the glossary's wording | V5.12 §11 / DECISIONS §9 (`d6d5c6e5`) | stronger: the old needles matched nothing (the test was vacuous) |
| O28 | `tests/frontend/test_nav_sheet_w2_c2.py:170-200` | the seat label is exact for a named account; a new test for a nameless one | V5.12 §11, WCAG 2.5.3 | stronger |
| O29 | `tests/frontend/test_terminology_v512_d.py:222-231` | the chip holds the rank, the step's title beside it | V5.18 lane D (one line on a phone) | stronger (added assertions) |
| O30 | `tests/frontend/test_console_shell_browser_w3_a.py:431-433` | «— Espace Personnes», not the role word «Personne» | V5.12 §11; DECISIONS §9 | exact |
| O31 | `test_console_shell_browser_w3_a.py:101-113` (fixture) and 6 tests; Academy last (:158) | `academy_published` publishes a course where «the ten» is measured | DECISIONS §8 (Academy hidden while 0 courses are published) | the feature enabled by a fixture, not a lowered count |
| O32 | `test_console_shell_browser_w3_a.py:179-199` (new) | without a course: the nine exact keys, and none in the drawer | DECISIONS §8 | new guard |
| O33 | `test_console_shell_browser_w3_a.py:575-580` | the company rail: count 10 became 6 exact keys | V5.13 Q7 («no person-oriented modules»); DECISIONS §8 | stronger (exact list) |
| O34 | `test_console_shell_browser_w3_a.py:632-636` | the institution and university rails: count 10 became 4 exact keys | V5.13 Q7 | stronger |
| O35 | `tests/frontend/test_overlays_console_browser_w2_a.py:67-78, :276-279` | `academy_published` for the drawer's last page | DECISIONS §8 | same |
| O36 | `tests/frontend/test_dashboard_browser_w3_b.py:388-391` | the institution's dashboard: `["deadlines", "messages", "organisation"]` | V5.13 Q7; DECISIONS §8 (empty modules hidden) | exact list |
| O37 | `test_dashboard_browser_w3_b.py:428-475` | empty registers: three pages, each held to its own kind and to exactly one empty state | V5.18 P-5; V5.15 lane B/D | stronger (it used to measure one page) |
| O38 | `test_console_shell_browser_w3_a.py:479-482`, `:868` | `legal_published` where the footer's legal line is measured | V5.13 Q2 / V5.14 §13 (D-16: only published legal pages are drawn) | the measure runs again (it raised a TypeError) |
| O39 | `test_console_shell_browser_w3_a.py:514-535` | the title on the atrium's inner edge (280 + 33), 34.72 px / 38.89 | DECISIONS §15 lane D (V5.15 §20), merged at `238dc1c` | exact values; one edge and one size for all five pages |
| O40 | `test_console_shell_browser_w3_a.py:883, :898` | the footer's links: 3 → 5 (four published legal pages + the address) | V5.13 Q2 / V5.14 §13 | same floors, more targets |
| O41 | `tests/frontend/test_mobile_rtl_w4_a.py:395-401, :448` | the pending targets move to the public privacy and cookie pages; condizioni and note legali assert 404 | DECISIONS §16 M-2 (V5.13 Q2) | stronger (404 asserted) |
| O42 | `test_mobile_rtl_w4_a.py:369-373, :427-431` | the companies' consent link measured in its step (painted as steps.js paints it); the removed «aiuto» line dropped from the list | V5.15 §15 / DL54-173 (steps engine); the aiuto line left with lane C's W2 composition (`4425219`, 28 Oct) | same floors, one more page (note: driving steps.js would bind it tighter) |
| O43 | `tests/i18n/test_routing.py:45-49` | floor 25 → 23, plus the exact gating of the three legal pages | V5.13 Q2 / V5.14; DECISIONS §16 M-2 | tight: 23 ungated routes counted here; the three are asserted, not dropped |
| O44 | `tests/i18n/test_rtl_browser.py:110-140` | «served ≥ 55» became the exact set of non-200 pages (3 × 404) and all 56 paths visited | DECISIONS §8 (V5.12 §13, Q6, Q8) | stronger: a 500 anywhere now fails (note: fixtures could open the three) |
| O45 | `tests/frontend/test_cms_nav.py:229-234` | Personnes: six entries with titles only (P-4); Entreprises: the duplicated sentence gone (B3) | V5.18 §2 (B3 by name); audit P-4 | exact pattern; the gloss asserted |
| O46 | `tests/frontend/test_header_fits_the_narrowest_viewport.py:141-150` | the name measured on /parcours/; the home asserts the mark alone at every width | V5.13 Q1 | same checks on two pages |
| O47 | `tests/i18n/test_rtl_browser.py:472-483` | wordmarks: ≥ 2 on Le projet and ≥ 1 on the home, all correct | V5.13 Q1 | same invariant on two pages |
| O48 | `tests/i18n/test_rtl_browser_nav.py:73-91` | N2 became the floating panel's three zones in both directions | V5.15 §1–§2; DL54-170 | exact geometry |
| O49 | `apps/pages/tests/test_institutional.py:94-96` | the trademark line's LTR isolate asserted | I18N-06 fixed in code (V5.18 §1, RTL) | stronger |
| O50 | `tests/frontend/test_browser_w2_c2.py:128-134` (LTR part) | the same start edge and rows; in LTR the mark does not move; the bar draws no words | V5.13 Q1 | exact (the RTL branch: V5) |
| O51 | `tests/frontend/test_entrance_w2_b.py:667-700` | sign-in: the central veil takes the page, the door rests; the keyboard path too | V5.18 §4 («login → platform», the central loader; P12) | exact on the new behaviour |
| O52 | `tests/frontend/test_loader_rules.py:369-371, :428` | the code anchors follow the veil hand-off | V5.18 §4 (P12) | same static strength |
| O53 | `tests/frontend/test_lume_v512_a.py:152-158` | the sign-in form no longer excluded; `after()` reports whether it took the page | V5.18 §4 (P12) | new assertion added |
| O54 | `tests/frontend/test_loader_w1_d.py:522-529` | the busy key read on the login button declared outcome-bearing; «no veil over the key» asserted | DL54-09 + V5.18 §4 | same component and fill (note: a real outcome-bearing form such as «Ma situation» would bind it tighter) |
| O55 | `tests/frontend/test_browser_chips_w1_c.py:387-404` | hover: the card lifts 3 px onto `--shadow-3`; a fixed 300 ms became a condition | V5.15 §6 («hover depth»); DL54-170 M15 | pinned to the token and the distance |
| O56 | `tests/frontend/test_browser_w1_c.py:438-450` | the FAQ mark: the drawn plus and minus, exact | V5.12 §6 (Accordion-09, `e2fe36ec`) | stronger than `!= "none"` |
| O57 | `tests/frontend/test_dashboard_browser_w3_b.py:49-65` | SETTLE awaits the finite `c-rise`; `_settle` waits for `lume-in` to end (5 s cap) | V5.15 §9–§11 (the veil), §20 | waits on a condition, not loosened guards |
| O58 | `tests/frontend/test_overlays_console_browser_w2_a.py:332-362` | the self-hidden children exactly `["lume-veil", "overlay-scrim"]`; the veil inert | V5.15 §8–§10 (the veil in base.html) | stronger |
| O59 | `tests/frontend/test_browser_w3_f1.py:26-45` | RADII_JS counts composed opacity < 0.01 as unseen (the veil warm at 0.002) | V5.15 lane A (pre-warmed veil, `lume.css:80-97`) | same invariant, what is seen (note: the extra `.closest('.lume-veil')` skip is redundant and could hide a stuck veil; drop it) |
| O60 | `tests/frontend/test_browser_w1_c.py:133-136` | the field radius in the formwork is 6 px; the formwork asserted | V5.15 §15 / DL54-173 | exact (it follows V6's outcome) |
| O61 | `tests/frontend/test_frontispiece_v515_c.py:279` | `text-align: right` became `end` | V5.18 T2 (fixed in code) | stronger (logical) |
| O62 | `tests/frontend/test_journey_w3_d.py:585-588` | `_compose.css` listed as a page modifier of the passage | DECISIONS §15 lane C (`a7884261`) | the «never a redrawing» check still runs over it |
| O63 | `tests/frontend/test_o14_lint.py:373` | `mfa/index.html`: `shield-check` (the 2FA page) | V5.18 P-2; CHECK_BEARING's existing `shield-check` entry | exact map |
| O64 | `tests/frontend/test_o14_lint.py:374-381` | `header.html`: one `check`, on the active language only (DL54-177) | see §4 item 2 | pinned (count 1, `l.active` only) |
| O65 | `tests/frontend/test_browser_w3_f1.py:89-141` | the door card: 7 sizes, the whole control inside the first screen, the question above the control | V5.18 §2 (B2 by name), §3 sizes; the review's polish 2 | stronger |
| O66 | ruff-only rewrites: `apps/ecosystem/tests/test_gated_pages.py`, `apps/pathways/tests/test_views.py`, `apps/portal/tests/test_views.py:102`, `apps/pages/tests/test_home.py:779-786, :873`, `tests/frontend/test_forms_v515_b.py:104` (C416) | wrapping and `list()`; values unchanged | V5.20 «0 blocking lint» | identical assertions |
| O67 | `tests/test_check_ownership.py:113-125, :386-421` | the family ids for v518-a…d, v519-k and v518g-n/c/p; 7 more refused ids | the process (DL54-175, 176, 179) | stronger (more refusals) |

## 6. The 8 skips and 2 xfails

The non-browser run at `e2098dd` (`evidence/v518/REGRESSION_GREEN_NONBROWSER.md`) had 8 skips and 2 xfails. The browser run had 0 skips.

| # | Test | Why it skips | Verdict | Action |
|---|---|---|---|---|
| 1 | `apps/cases/tests/test_intake.py::test_the_legal_layer_supplies_the_sources_the_questionnaire_cannot` (:133) | no legal rule in force applies | **should run with a fixture** | a test-only rule in force, with a TEST FIXTURE source and a precise reference, on the pathway the seeded questionnaire reaches. The rules tests already build in-force `LegalRule` rows (`apps/rules/tests/test_governance.py:54`, TestValidity). Keep one test of the pre-production truth (no rule in force, no applied rule) |
| 2 | `…::test_an_outcome_stronger_than_possible_can_say_which_rule_made_it_so` (:209) | the run did not reach a stronger outcome | **should run with a fixture** | the same fixture, with a rule that raises the outcome |
| 3 | `…::test_a_legal_requirement_becomes_a_checklist_line_carrying_its_source` (:238) | no rule found a missing requirement | **should run with a fixture** | the same fixture, with a rule carrying a requirement |
| 4–7 | `apps/pages/tests/test_contact_channels_v519.py::test_no_obsolete_number_on_a_public_page[faq/-fr\|it\|en\|ar]` (:153) | `/faq/` answers 404 in the seeded database | **should run with a fixture** (and is V11) | `phase3_open` + `seed_locked_faq_items()`, then assert 200 |
| 8 | `tests/security/test_confidential_material.py::test_the_depositants_private_identifiers_are_checked` (:224) | `ILE_CONFIDENTIAL_SENTINELS` is not set (CI and a fresh clone) | **genuinely environment-bound.** By the owner's design the private table never enters the repository or CI; the skip prints its reason | keep it. It must run before a push, with the table configured; today its sibling is red there (V13) |
| x1 | XFAIL (strict) `tests/frontend/test_design_showcase.py::test_every_caption_is_the_value_its_swatch_paints` (:231) | `apps/core/dev.py` prints its captions from `static/css/v2/tokens.css`; 14 of 44 name a hex no page paints | **debt** (since 5 Oct, `daf9165`); not environment-bound | print the captions from the effective cascade, as the test models it, and drop the marker. It is strict, so a fix cannot go unnoticed |
| x2 | XFAIL (`strict=False`) `tests/frontend/test_legacy_token_shim.py::test_the_shim_is_gone` (:131) | the legacy shim still exists | **debt** (since 21 Sep); not environment-bound | make it `strict=True`. The shim's names that nothing reads are also the cheapest bytes for V1 |

Once V11 and rows 1–3 are converted, only row 8 remains as a skip: genuinely environment-bound, so UNEXPECTED SKIPS = 0.

## 7. Observations outside the test diff (for the fixing lanes)

- **Fills still left on time-based animations.** These can surface once V3 and V4 are restored. Animations with a duration that fill `both` or `forwards`:
  - `_fronte.css:328, 334, 348, 360, 526, 1363, 1373, 1385, 1389, 1393, 1401, 1405`;
  - `_formwork.css:118`;
  - `_receipt.css:41`;
  - `_reveal.css:66, 94, 289, 294`;
  - `chrome.css:837, 840, 846, 851`;
  - `loader.css:123, 208, 246`;
  - `_loader-light.css:24-37`.

  The `linear both` rules in `_reveal.css:164-438` and `_photo.css:84` are scroll-driven and are not in scope. Each fill needs a triage under V5.20's motion rule: where the end state is the natural one, `backwards`; the loader's deliberate hold stays.
- **Bespoke shadows in `_fronte.css`:** :517, 561, 665, 946, 997, 1118 and 1205. Group N replaced their literal colours with `color-mix()` over the palette primitive `--p-notte-950`, which is the same colour and passes the colour guard. Their geometry is still outside the `--shadow-*` hierarchy (see V7 and V8). Note also that `--passe-partout` already exists as a token (`tokens.css:418`, an inset hairline), but the head photograph does not use it.
- **`icons.CHROME_SPRITE_MAX_BYTES = 31_049`** says it «only ratchets down». The chrome sprite now weighs 17 464 B (up 425 B for `message-circle`). The ceiling has never been re-seated at the measure. This is not changed in the range, but it is a slack ratchet of the same kind as V2.
- **`shell.js`** is 4 694 B gzip against its 4 700 budget. That is not a violation, but it leaves almost no headroom.

## 8. Sources read

**Owner directives:** `V5_20`, `V5_18`, `V5_19`, `V5_17`, `V5_15`, `V5_13`, `V5_12`, `V5_8`, and the corner passages of `V5_1` and `V5_2`.

**Director and decision log:**

- `.work/v512-audit/director/DECISIONS.md` (§5.7, §8, §9, §15, §16, Lane B acceptance);
- `docs/design-v5/DECISION_LOG_V54.md`, DL54-170 to DL54-179.

**Evidence:**

- `evidence/v518/AUDIT_quality.md` (P-3, P-4);
- `INTEGRATED_REVIEW.md`;
- `REGRESSION_NONBROWSER.md`, `REGRESSION_GREEN_NONBROWSER.md`, `REGRESSION_GREEN_BROWSER.md`;
- `workflows_v515/v518_findings.json` (T1–T3, with the orchestrator's «update without weakening» prescriptions, made before V5.20);
- `.work/v518g-p/probe_formwork.json`, `probe_public.json`.

**Code and tests:**

- `git diff 238dc1c..e2098dd` for every test file and every conftest;
- the per-commit history of the guards cited above;
- the product sheets cited above (`tokens.css`, `_formwork.css`, `_steps.css`, `_glyph.css`, `_fronte.css`, `lume.css`, `chrome.css`, `_motion.css`), plus `apps/core/icons.py`, `apps/accounts/shell.py`, `templates/components/breadcrumbs.html` and `templates/partials/header.html`.

**Measures taken here:**

- main.css gzip -9 at each milestone: 33 448 → 33 455 → 33 572 → 33 579 → 33 406 → 33 530;
- the ceiling at each milestone: 33 448 → 33 576 → 33 600 → 33 530;
- 23 ungated public routes and 56 distinct paths, counted without a database.

**Scratch files:** `C:/tmp/ile_v5_council/.work/v520-audit/` (`tests.diff`, `all.diff`, `count_routes.py`).
