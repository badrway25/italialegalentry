# main.css — the rules no coverage scenario used (v520-css, 30 October 2026)

Chromium rule-usage coverage (CDP `CSS.startRuleUsageTracking` / `takeCoverageDelta`) of the ORIGINAL
`static/css/dist/main.css` (design-v5 `e2098dd`, 173 813 B, 33 530 B gzip -9) on the lane server 8785 (`ile_v5_l5`, a copy
of the preview database, the nine acceptance personas): 1320 scenarios — err 24, fc 80, fine390 40, land 40, nav 8, per 288, post 32, pr 40, pub 328, rm 80, wid 360.
pub = every public route × fr/it/en/ar × 1440/390 (scrolled, the doors or the sheet and its doors opened, every `<details>`,
popover and dialog opened, ten Tab presses, hover/focus/focus-visible/active forced on 260 distinct elements, every form's
submit pressed and its fields filled); per = every persona page of the index (9 personas) × 1440/390, same interactions;
wid = 20 pages × fr/ar × 1680/1280/1100/1024/900/768/600/360/320; land = 844 × 390; rm / fc = reduced motion / forced colours
× 1440/390; pr = print; fine390 = a phone width with a fine pointer; post = the server's own error state of eight forms posted
empty; nav = a real page change answered 2.2 s late (the Lume veil, the doorway, the key, the light); err = the 400/403/404/500
pages, the preview's 404/429, the specimens and the dev showcase.

195 of 999 style rules were never used (17 753 B raw). Each was checked against its producers (templates' class
attributes and tag arguments, JavaScript strings and class toggles, Python strings; the CMS content is escaped text with no
`class=`): the verdict column says what came of it. «Produced» rules are live behaviour the run could not reach (a signed-in
public page, a staff or moderator surface, an uploaded logo, a toast leaving, a hover under a fine pointer that was not
forced, a disabled control, `html.no-js`, print, a slow navigation's phases …); they stay.

| Source | Bytes | Context | Selector | Verdict |
|---|---|---|---|---|
| `static/css/_legacy-tokens.css:185` | 56 | — | `:lang(ar) .eyebrow` | produced — a state, page or role the run did not reach — kept |
| `static/css/_legacy-tokens.css:190` | 107 | — | `.numeral` | **dead — removed** |
| `static/css/base.css:64` | 30 | — | `iframe` | produced — a state, page or role the run did not reach — kept |
| `static/css/base.css:104` | 108 | — | `hr` | produced — a state, page or role the run did not reach — kept |
| `static/css/base.css:115` | 26 | — | `address` | produced — a state, page or role the run did not reach — kept |
| `static/css/base.css:119` | 73 | — | `abbr[title]` | produced — a state, page or role the run did not reach — kept |
| `static/css/base.css:152` | 246 | — | `.t-plate` | dead (no producer) but documented in DESIGN_SYSTEM_2026 — kept, listed for the steward |
| `static/css/base.css:232` | 193 | — | `.lead` | produced — a state, page or role the run did not reach — kept |
| `static/css/base.css:399` | 217 | — | `.prose blockquote` | produced — a state, page or role the run did not reach — kept |
| `static/css/base.css:407` | 43 | — | `.prose table` | produced — a state, page or role the run did not reach — kept |
| `static/css/base.css:411` | 160 | — | `.prose th,.prose td` | produced — a state, page or role the run did not reach — kept |
| `static/css/base.css:419` | 114 | — | `.prose th` | produced — a state, page or role the run did not reach — kept |
| `static/css/base.css:425` | 38 | — | `.prose figure` | produced — a state, page or role the run did not reach — kept |
| `static/css/base.css:429` | 108 | — | `.prose figcaption` | produced — a state, page or role the run did not reach — kept |
| `static/css/base.css:436` | 44 | — | `[lang=fr]:not(:lang(fr))` | produced — a state, page or role the run did not reach — kept |
| `static/css/components.css:55` | 84 | — | `.icon--hero` | produced — a state, page or role the run did not reach — kept |
| `static/css/components.css:137` | 112 | — | `.institutional-banner` | produced — a state, page or role the run did not reach — kept |
| `static/css/components.css:142` | 124 | — | `.institutional-banner__inner` | produced — a state, page or role the run did not reach — kept |
| `static/css/components.css:150` | 75 | (min-width:64rem) | `.institutional-banner__inner` | produced — a state, page or role the run did not reach — kept |
| `static/css/components.css:155` | 185 | — | `.institutional-banner__title` | produced — a state, page or role the run did not reach — kept |
| `static/css/components.css:164` | 173 | — | `.institutional-banner__meta` | produced — a state, page or role the run did not reach — kept |
| `static/css/components.css:172` | 206 | — | `.institutional-banner__quote` | produced — a state, page or role the run did not reach — kept |
| `static/css/components.css:181` | 63 | — | `.institutional-banner__actions` | produced — a state, page or role the run did not reach — kept |
| `static/css/components.css:295` | 90 | — | `.pagination__link:hover` | produced — a state, page or role the run did not reach — kept |
| `static/css/components.css:363` | 48 | (forced-colors:active) | `.empty-state__icon` | produced (`{% svg_icon … "… class" %}`) — kept |
| `static/css/layout.css:34` | 71 | — | `.zones` | dead (no producer) but documented in DESIGN_SYSTEM_2026 — kept, listed for the steward |
| `static/css/layout.css:41` | 130 | (min-width:75rem) | `.zones` | dead (no producer) but documented in DESIGN_SYSTEM_2026 — kept, listed for the steward |
| `static/css/layout.css:63` | 43 | — | `.section` | produced — a state, page or role the run did not reach — kept |
| `static/css/layout.css:87` | 99 | — | `.grid` | produced — a state, page or role the run did not reach — kept |
| `static/css/layout.css:93` | 46 | — | `.grid>*` | produced — a state, page or role the run did not reach — kept |
| `static/css/layout.css:99` | 30 | (min-width:64rem) | `.lg\:col-3` | dead (no producer) but documented in DESIGN_SYSTEM_2026 — kept, listed for the steward |
| `static/css/layout.css:100` | 30 | (min-width:64rem) | `.lg\:col-4` | dead (no producer) but documented in DESIGN_SYSTEM_2026 — kept, listed for the steward |
| `static/css/layout.css:101` | 30 | (min-width:64rem) | `.lg\:col-6` | dead (no producer) but documented in DESIGN_SYSTEM_2026 — kept, listed for the steward |
| `static/css/layout.css:102` | 30 | (min-width:64rem) | `.lg\:col-8` | dead (no producer) but documented in DESIGN_SYSTEM_2026 — kept, listed for the steward |
| `static/css/layout.css:108` | 109 | — | `.split` | produced — a state, page or role the run did not reach — kept |
| `static/css/layout.css:116` | 57 | (min-width:56rem) | `.split` | produced — a state, page or role the run did not reach — kept |
| `static/css/layout.css:122` | 47 | — | `.stack>*+*` | produced — a state, page or role the run did not reach — kept |
| `static/css/layout.css:134` | 26 | — | `.center` | produced — a state, page or role the run did not reach — kept |
| `static/css/layout.css:138` | 46 | — | `.measure` | produced — a state, page or role the run did not reach — kept |
| `static/css/layout.css:142` | 44 | — | `.flow>*+*` | produced — a state, page or role the run did not reach — kept |
| `static/css/layout.css:146` | 40 | — | `.mt-4` | produced — a state, page or role the run did not reach — kept |
| `static/css/layout.css:147` | 38 | — | `.mb-4` | produced — a state, page or role the run did not reach — kept |
| `static/css/layout.css:148` | 38 | — | `.mb-8` | produced — a state, page or role the run did not reach — kept |
| `static/css/layout.css:151` | 111 | — | `.rule` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:135` | 38 | — | `.jurisdiction` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:139` | 81 | — | `.jurisdiction__bar` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:145` | 81 | — | `.jurisdiction__segment` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:153` | 51 | — | `.jurisdiction__segment[data-share="1"]` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:157` | 51 | — | `.jurisdiction__segment[data-share="2"]` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:161` | 51 | — | `.jurisdiction__segment[data-share="3"]` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:165` | 51 | — | `.jurisdiction__segment[data-share="4"]` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:169` | 51 | — | `.jurisdiction__segment[data-share="5"]` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:173` | 51 | — | `.jurisdiction__segment[data-share="6"]` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:177` | 54 | — | `.jurisdiction__segment:last-child` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:184` | 156 | — | `.jurisdiction__segment--morocco` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:193` | 148 | — | `.jurisdiction__segment--italy` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:202` | 62 | — | `.jurisdiction__segment--platform` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:206` | 150 | — | `.jurisdiction__segment--authority` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:215` | 250 | — | `.jurisdiction__legend` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:228` | 66 | — | `.jurisdiction__key` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:234` | 98 | — | `.jurisdiction__swatch` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:252` | 85 | — | `.plate` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:277` | 188 | — | `.gloss` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:286` | 40 | — | `.gloss>li` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:340` | 43 | — | `.sources__consulted` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:367` | 68 | — | `.outcome--missing` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:371` | 65 | — | `.outcome--warning` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:375` | 63 | — | `.outcome--stop` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:379` | 64 | — | `.outcome--review` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:418` | 39 | (forced-colors:active) | `.sources__item:before` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:424` | 112 | (forced-colors:active) | `.jurisdiction__segment,.jurisdiction__swatch` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:431` | 46 | (forced-colors:active) | `.outcome` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:451` | 49 | — | `.entry:not(a) .entry__title` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:455` | 49 | — | `.jurisdiction__title` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:459` | 53 | — | `.jurisdiction__caption` | produced — a state, page or role the run did not reach — kept |
| `static/css/register.css:467` | 45 | — | `.plate:has(+.home-banner)` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/base.css:24` | 50 | — | `.lead` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/base.css:40` | 106 | — | `:root .hero__title[translate=no]` | **dead — removed** |
| `static/css/v5/base.css:58` | 107 | — | `:root body :is(.forum-programme__note,.forum-banner__quote,.institutional-banner__quote)` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/base.css:106` | 67 | — | `:lang(ar) :is(em,i)` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/base.css:113` | 57 | — | `:lang(ar) .entrance .form-field__help` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/buttons.css:134` | 98 | — | `.btn--upper` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/buttons.css:135` | 59 | — | `:lang(ar) .btn--upper` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/buttons.css:225` | 157 | — | `:is(.hero,.chapter--dark,.on-inverse,.forum-cta,.forum-hero,.forum-banner) .btn--danger,.btn--inverse.btn--danger` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/buttons.css:234` | 202 | — | `:is(.hero,.chapter--dark,.on-inverse,.forum-cta,.forum-hero,.forum-banner) :is(.btn--link,.btn--text),.btn--inverse:i…` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/buttons.css:245` | 143 | — | `:is(.btn--ghost,.btn--link,.btn--text,.btn--icon):is(:disabled,[aria-disabled=true],.is-disabled)` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/buttons.css:272` | 143 | (prefers-reduced-motion:reduce) | `.btn:active,.btn--arrow:hover .icon,.link-arrow:hover .icon,[dir=rtl] .btn--arrow:hover .icon,[dir=rtl] .link-arrow:h…` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/buttons.css:287` | 33 | (forced-colors:active) | `.btn--danger` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/buttons.css:290` | 111 | (forced-colors:active) | `.btn:is(:disabled,[aria-disabled=true],.is-disabled)` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/card.css:105` | 62 | — | `.card--link .card__meta>:any-link` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/card.css:144` | 53 | (hover:hover) | `.card--link:hover` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/card.css:148` | 116 | (hover:hover) | `.card--link:hover .card__title a` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chip.css:162` | 25 | print | `.chip` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:145` | 74 | (hover:hover)and (pointer:fine) | `.lang-seg__list--names .lang-seg__link:hover` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:146` | 71 | (hover:hover)and (pointer:fine) | `.lang-seg__list--names .lang-seg__link:hover:after` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:218` | 48 | — | `.brand__logo` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:309` | 198 | — | `html.no-js .main-nav[data-portico] .main-nav__link:after` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:318` | 118 | — | `html.no-js .main-nav[data-portico] .main-nav__link:is([aria-current],:hover,:focus-visible):after` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:386` | 38 | (min-width:64rem)and (max-width:79.999rem) | `.site-header .lock__wm` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:431` | 53 | (hover:hover)and (pointer:fine) | `.portico__link:hover` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:432` | 62 | (hover:hover)and (pointer:fine) | `.portico__link:hover .portico__title` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:436` | 46 | — | `.portico__link:focus-visible` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:449` | 83 | (hover:hover) | `.portico__space:hover` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:572` | 65 | (min-width:48rem)and (max-width:89.999rem) | `.targa-seat .account-menu__summary .icon:last-child` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:675` | 53 | — | `.nav-sheet__row::-webkit-details-marker` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:686` | 47 | (hover:hover)and (pointer:fine) | `.nav-sheet__row:hover` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:695` | 58 | — | `.nav-sheet__panel .portico__glyph:empty` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:748` | 65 | (hover:hover)and (pointer:fine) | `.nav-sheet__field-go:hover` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:785` | 139 | (hover:hover)and (pointer:fine) | `:is(.targa--night,.nav-sheet__foot .account-menu__summary):hover` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:825` | 237 | — | `.nav-sheet__photo` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:837` | 98 | (prefers-reduced-motion:no-preference) | `.nav-sheet__door[open] .nav-sheet__photo` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:999` | 100 | (hover:hover)and (pointer:fine) | `.nav-sheet__channel:hover` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:1012` | 51 | (prefers-reduced-motion:reduce) | `.main-nav.is-first .portico__entry` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:1013` | 64 | (prefers-reduced-motion:reduce) | `.portico__photo` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/chrome.css:1034` | 66 | print | `.main-nav,.site-header__end,.portico-scrim` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/field.css:47` | 124 | — | `.form__required-note` | dead (no producer) but documented in DESIGN_SYSTEM_2026 — kept, listed for the steward |
| `static/css/v5/field.css:124` | 133 | — | `.form-field :is(input,select,textarea):autofill` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/field.css:140` | 66 | — | `.form-field select:is([multiple],[size])` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/field.css:161` | 136 | — | `::-webkit-calendar-picker-indicator:focus-visible` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/field.css:165` | 229 | (hover:hover) | `.form-field :where(input:not([type=checkbox],[type=radio],[type=file]),select,textarea):hover:not(:disabled,:focus-vi…` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/field.css:207` | 56 | — | `.form-field__errors li+li` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/field.css:222` | 186 | — | `.form-field :where(input,select,textarea):disabled,.input:disabled` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/field.css:264` | 78 | — | `.form-field__toggle[aria-pressed=true] .form-field__toggle-hide` | produced (`{% svg_icon … "… class" %}`) — kept |
| `static/css/v5/field.css:314` | 175 | — | `:where(input[type=checkbox],input[type=radio]):disabled` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/field.css:316` | 178 | — | `:where(input[type=checkbox][role=switch])` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/field.css:317` | 163 | — | `:where(input[type=checkbox][role=switch]):before` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/field.css:318` | 110 | — | `:where(input[type=checkbox][role=switch]):checked:before` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/field.css:319` | 97 | — | `[dir=rtl] :where(input[type=checkbox][role=switch]):checked:before` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/field.css:349` | 80 | (forced-colors:active) | `.form-field select:not([multiple],[size])` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/field.css:354` | 62 | (forced-colors:active) | `.form-field__toggle[aria-pressed=true]` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/loader.css:145` | 35 | — | `.loader__status:empty` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/loader.css:149` | 83 | — | `:is(.chapter--dark,.on-inverse,.hero) .loader__status` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/loader.css:249` | 84 | — | `.is-lit .busy-key` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/loader.css:265` | 85 | — | `[data-seat].is-seating>:nth-child(5)` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/loader.css:266` | 85 | — | `[data-seat].is-seating>:nth-child(6)` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/loader.css:267` | 85 | — | `[data-seat].is-seating>:nth-child(7)` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/loader.css:268` | 87 | — | `[data-seat].is-seating>:nth-child(n+8)` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/loader.css:293` | 71 | (forced-colors:active) | `.btn.is-busy:after,.busy-key` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:262` | 58 | — | `:is(.lume-go,.is-departing) .lume-veil` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:266` | 88 | — | `.lume-go .lume-veil__ground` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:270` | 86 | — | `.lume-go .lume-veil__stage` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:280` | 76 | — | `.lume-go .lume-veil__sig .sig__turn` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:284` | 80 | — | `.lume-go .lume-veil__sig .sig__turn:before` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:289` | 123 | (prefers-reduced-motion:no-preference) | `html:not(.rm).lume-go.is-departing .lume-veil__sig .sig__turn` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:295` | 91 | — | `.is-departing .lume-veil__sill` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:299` | 100 | — | `.is-departing .lume-veil__sig .sig__lume` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:304` | 103 | — | `.is-departing:not(.lume-go) .lume-veil__ground,.is-departing:not(.lume-go) .lume-veil__stage` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:309` | 102 | — | `[data-input=key].is-departing :is(.lume-veil__sill,.lume-veil__sig .sig__lume)` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:468` | 78 | — | `.lume-go .lume-veil__sig .sig__key` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:483` | 97 | (prefers-reduced-motion:reduce) | `.lume-go .lume-veil__ground,.lume-go .lume-veil__stage` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:521` | 337 | — | `html.rm:is(.lume-go,.is-departing,.lume-in,.lume-first) .lume-veil,html.rm:is(.lume-go,.is-departing,.lume-in,.lume-f…` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:527` | 98 | — | `html.rm:is(.lume-go,.is-departing) .lume-veil :is(.lume-veil__ground,.lume-veil__stage)` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:531` | 85 | — | `html.rm:is(.lume-go,.is-departing) .lume-veil .lume-veil__sill` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:535` | 82 | — | `html.rm:is(.lume-go,.is-departing) .lume-veil .sig__lume` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:545` | 88 | — | `html.rm .lume-veil .sig__turn:before,html.rm .lume-veil .sig__turn:after` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:553` | 61 | (min-width:64rem) | `html.lume-pane body.console` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:557` | 105 | (min-width:64rem) | `html.lume-pane body.console :is(.lume-veil,.lume-veil__word)` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/lume.css:561` | 258 | (min-width:64rem) | `html.lume-pane body.console .lume-veil__ground` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/motion.css:168` | 66 | — | `.messages--toast .alert` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/motion.css:174` | 110 | — | `.alert.is-leaving` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/motion.css:180` | 67 | — | `.messages--toast .alert.is-leaving` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/motion.css:184` | 59 | — | `[data-input=key] .alert.is-leaving` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/notice.css:35` | 36 | — | `.messages` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/notice.css:36` | 41 | — | `.messages:not(:has(.alert))` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/notice.css:41` | 35 | — | `.alert>.notice__icon` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/notice.css:42` | 58 | — | `.alert__text` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/notice.css:44` | 89 | — | `.alert__close` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/notice.css:49` | 174 | — | `html.js .messages--toast` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/notice.css:56` | 146 | — | `html.js .messages--toast .alert` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/notice.css:58` | 127 | (max-width:63.999rem) | `html.js body.console .messages--toast` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/notice.css:99` | 58 | — | `.form-unavailable` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/notice.css:114` | 62 | (forced-colors:active) | `.notice--error,.alert--error` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/overlays.css:116` | 59 | (hover:hover)and (pointer:fine) | `.overlay__item:hover` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/overlays.css:118` | 84 | — | `.overlay__item:active` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/overlays.css:181` | 46 | — | `.overlay-scrim[data-held]` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/overlays.css:369` | 22 | (max-width:40rem) | `.tooltip` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/overlays.css:386` | 36 | — | `html.no-js .overlay` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/overlays.css:387` | 119 | — | `html.no-js .overlay:target` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/overlays.css:420` | 50 | (forced-colors:active) | `.overlay__sep` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/overlays.css:421` | 58 | (forced-colors:active) | `.tooltip` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/overlays.css:468` | 60 | — | `.account-menu__summary::-webkit-details-marker` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tabs.css:35` | 36 | — | `html.no-js .tabs__list` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tabs.css:49` | 37 | (hover:hover) | `.tabs__tab:hover` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tabs.css:50` | 76 | — | `.tabs__tab:focus-visible` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tabs.css:76` | 110 | — | `.tabs.is-travelling .tabs__list:after` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tabs.css:77` | 114 | — | `body.console .tabs.is-travelling .tabs__list:after` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tabs.css:80` | 117 | — | `html.no-js .tabs .tabs__panel` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tabs.css:81` | 53 | — | `.tabs__panel:focus-visible` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tabs.css:96` | 211 | — | `.tabs.is-travelling .tabs__panel` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tabs.css:98` | 123 | — | `.tabs.is-travelling .tabs__panel` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tabs.css:124` | 57 | — | `.accordion__summary::-webkit-details-marker` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tabs.css:156` | 101 | (forced-colors:active) | `.tabs__tab[aria-selected=true]:after,.tabs__list:after` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tokens.css:502` | 332 | — | `html.rm` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tokens.css:734` | 182 | (forced-colors:active) | `[data-register][data-register],:is(.on-inverse,.rail,.tooltip,.site-footer) [data-register]` | produced — a state, page or role the run did not reach — kept |
| `static/css/v5/tokens.css:736` | 148 | (forced-colors:active) | `[data-register=nullo][data-register],:is(.on-inverse,.rail,.tooltip,.site-footer) [data-register=nullo]` | produced — a state, page or role the run did not reach — kept |
