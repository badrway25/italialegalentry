# 21ST.DEV SEARCH LOG — merged (V5)

**Italy Legal Entry™ · Executive Creative Director · 27 September 2026.** Every 21st.dev lookup made by the V5 council, merged from the five family curations and the motion and mobile lanes, deduplicated by query. Parsed from the reports' own search-log tables by `scratch/ecd/parse_searchlog.py`; nothing here was re-run. **This role made no 21st call.** `generate` and `iterate_generation` were called **0** times by every lane (each lane states it; the owner reserved the AI-generation credits).

## 1. Totals per lane

| Lane (report) | `search` | `get_inspiration` | Lookups | `get_component` | Preview images looked at | Candidates registered | `generate` / `iterate_generation` |
|---|---|---|---|---|---|---|---|
| nav-shell (`21st_nav-shell.md`) | 30 | 2 | 32 | 23 | 21 | 99 | 0 / 0 |
| hero-public (`21st_hero-public.md`) | 35 | 2 | 37 | 16 | 65 | 86 | 0 / 0 |
| primitives (`21st_primitives.md`) | 40 | 2 | 42 | 26 | 16 | 192 | 0 / 0 |
| forms-docs (`21st_forms-docs.md`) | 26 | 2 | 28 | 15 | 54 | 130 | 0 / 0 |
| platform-domains (`21st_platform-domains.md`) | 28 | 2 | 30 | 13 | 19 | 93 | 0 / 0 |
| motion (`MOTION.md` §14.6) | 4 | 0 | 4 | 3 | 0 | — | 0 / 0 |
| mobile (`MOBILE_UX.md` §1.4) | 2 | 0 | 2 | 1 | 0 | — | 0 / 0 |
| **Total** | **165** | **10** | **175** | **97** (89 distinct ids) | **175** | **600** rows · 544 distinct | **0 / 0** |

Notes: result rows returned by the lookups ≈ 3 050 (nav ≈ 680 · hero 450 · primitives 762 · forms 560 · platform 640), duplicates across queries included; preview **videos** watched: 0 in every lane (motion was judged from retrieved code); `get_inspiration` ran without a project design context in the curations that say so (`contextApplied: false`), so its ranking is generic; one query text was run by two lanes («command palette», nav-shell and platform-domains).

## 2. The merged query log

Sorted by lane then by the lane's own order. **Used** = the candidates the lane selected from that query (as the lane wrote it; «—» = nothing selected, the query only fed rejections or confirmations).

| # | Lane | Tool | Query | Results | Used |
|---|---|---|---|---|---|
| 1 | nav-shell | search | premium navigation motion mega menu | 30 | #31723, #31509, #21349 |
| 2 | nav-shell | search | floating navbar | 30 | #27428 |
| 3 | nav-shell | search | kinetic navigation | 30 | — |
| 4 | nav-shell | search | fluid menu | 20 | — |
| 5 | nav-shell | search | animated dropdown navigation | 30 | #22313 (drawer idea) |
| 6 | nav-shell | search | responsive mega menu | 30 | #31723 |
| 7 | nav-shell | search | dashboard collapsible sidebar premium | 30 | #29334, #21517 |
| 8 | nav-shell | search | premium application shell | 30 | — |
| 9 | nav-shell | search | nested dashboard menu | 20 | #19009 |
| 10 | nav-shell | search | limelight nav | 15 | #9952 (image-swap idea) |
| 11 | nav-shell | search | dock navigation | 15 | #29954 |
| 12 | nav-shell | search | resizable navbar | 15 | — |
| 13 | nav-shell | search | command palette *(also run by another lane)* | 30 | #27378 |
| 14 | nav-shell | search | search overlay premium | 30 | #31184, #11338, #29989 |
| 15 | nav-shell | search | language switcher locale selector | 20 | — (catalogue gap) |
| 16 | nav-shell | search | breadcrumb | 20 | #29229 |
| 17 | nav-shell | search | scroll progress indicator reading bar | 20 | #18715 (values) |
| 18 | nav-shell | search | page transition route change view transition | 20 | #18251 (values) |
| 19 | nav-shell | search | mobile drawer menu full screen navigation accordion | 20 | #23558 (model) |
| 20 | nav-shell | search | user account menu avatar dropdown sign in | 20 | #393 |
| 21 | nav-shell | search | dashboard top header bar breadcrumb search notifications | 20 | #18149 |
| 22 | nav-shell | search | mega menu featured image card dropdown | 20 | — |
| 23 | nav-shell | search | segmented control sliding indicator | 15 | #23552 |
| 24 | nav-shell | search | table of contents scroll spy active section | 15 | #18113 |
| 25 | nav-shell | search | top loading bar navigation progress nprogress | 15 | — |
| 26 | nav-shell | search | mobile bottom tab bar app navigation | 15 | #27897 |
| 27 | nav-shell | get_inspiration | institutional public-service header, mega menu, photo per section, 4 languages incl. RTL, reserved-area login | 12 | confirms #31723/#31509; adds #26888 |
| 28 | nav-shell | get_inspiration | case-management portal app shell: rail, context bar, account, bottom bar, drawer | 12 | confirms #29334 |
| 29 | nav-shell | search | collapsed icon rail sidebar tooltip keyboard accessible navigation | 20 | #31328 (collapsed-rail tooltip reference; no new shell candidate) |
| 30 | nav-shell | search | sticky header shrink on scroll logo scale transparent to solid | 20 | #23562 (platform context-bar title) · #16834 (loading, brand-asset gate) |
| 31 | nav-shell | search | navigation link hover image preview reveal editorial menu | 20 | #28258 (row anatomy only) · #26256 confirms the fixed-slot swap of #9952 |
| 32 | nav-shell | search | app layout skeleton loading state page shell placeholder | 20 | #23557 (timing + zero-CLS rules) · #19026 (rail region reference) |
| 33 | hero-public | search | animated institutional hero | 30 | — |
| 34 | hero-public | search | liquid metal hero | 15 | — |
| 35 | hero-public | search | dynamic hero | 20 | — |
| 36 | hero-public | search | video hero premium | 15 | #24752 idea → gallery only |
| 37 | hero-public | search | grain gradient hero | 12 | **#24379** |
| 38 | hero-public | search | animated shader hero | 12 | — |
| 39 | hero-public | search | woven light hero | 8 | — |
| 40 | hero-public | search | glassmorphism trust hero | 8 | — |
| 41 | hero-public | search | scroll morph hero | 8 | **#2061** |
| 42 | hero-public | search | cinematic landing hero | 10 | — |
| 43 | hero-public | search | aether hero | 6 | — |
| 44 | hero-public | search | spatial product showcase | 8 | #9679 (re-tint idea) |
| 45 | hero-public | search | editorial hero serif headline photography mask reveal | 12 | **#19077, #10905** |
| 46 | hero-public | search | architectural arch image hero | 10 | #19080 (mask-fade idea) |
| 47 | hero-public | get_inspiration | premium institutional legal-tech hero, navy/teal, serif, arch, four routes… | 12 | confirms editorial-serif direction |
| 48 | hero-public | search | audience selector cards persona segments who are you | 15 | — |
| 49 | hero-public | get_inspiration | four audience entry panels with photo, icon, accent, hover reveal… | 10 | #27010 mechanics, #30554 focus parity |
| 50 | hero-public | search | interactive image accordion expanding panels | 12 | #27010 |
| 51 | hero-public | search | spotlight card hover gradient border grid | 12 | **#26797** |
| 52 | hero-public | search | bento grid premium | 15 | #18898 layout only |
| 53 | hero-public | search | bento grid with images editorial | 10 | spans recipe only |
| 54 | hero-public | search | ecosystem integration diagram connected nodes beams | 10 | — |
| 55 | hero-public | search | partners logo cloud institutional | 10 | — (names list; logos only if `logo_public`/G6) |
| 56 | hero-public | search | feature section premium | 15 | — |
| 57 | hero-public | search | sticky scroll image text section parallax | 12 | **#18041** |
| 58 | hero-public | search | cta section premium | 15 | **#28147** |
| 59 | hero-public | search | cta banner with background image dark overlay | 10 | #16730 overlay recipe |
| 60 | hero-public | search | faq accordion elegant | 15 | — (native `<details>` kept) |
| 61 | hero-public | search | faq section two column with categories | 10 | **#26656 + #26910** |
| 62 | hero-public | search | footer premium | 15 | **#21474 + #29773** |
| 63 | hero-public | search | news blog cards section image editorial | 15 | **#28595** (+#9321 fallback) |
| 64 | hero-public | search | process steps timeline scroll animated | 15 | **#28273** |
| 65 | hero-public | search | route map journey path stations svg animated | 10 | **#24528** (+#24556 option) |
| 66 | hero-public | search | event conference section schedule speakers | 6 | #25369 facts grammar |
| 67 | hero-public | search | conference event landing hero date venue register | 10 | — |
| 68 | hero-public | search | speakers grid team portraits hover | 10 | **#10098** |
| 69 | hero-public | search | video player media section gallery lightbox | 12 | **#27093 + #4586** |
| 70 | primitives | search | liquid metal button premium institutional | 30 | #29293 rim (tier 1) + engine of #10443 (tier 2) |
| 71 | primitives | search | interactive hover button | 20 | arrow nudge only (already V4) |
| 72 | primitives | search | shiny button | 20 | inset-light idea only |
| 73 | primitives | search | tactile button | 20 | 1 px inner light (#24399) |
| 74 | primitives | search | glow button | 20 | none |
| 75 | primitives | search | animated gradient button | 20 | #25501 layered inset lighting (detail) |
| 76 | primitives | search | elegant outline ghost button minimal | 20 | V4 GHOST/OUTLINE confirmed |
| 77 | primitives | search | button system variants primary secondary soft ghost destructive loading success | 20 | #23536 state cell + coss coarse-pointer hit area |
| 78 | primitives | search | icon button with tooltip accessible | 15 | V4 IconButton + arrowless tooltip |
| 79 | primitives | search | destructive button confirm hold to delete | 15 | DESTRUCTIVE + dialog; typed confirm for irreversible acts |
| 80 | primitives | search | status badges modern | 30 | V4 register pill + coss/Tremor anatomy |
| 81 | primitives | search | document status badge with icon approved pending rejected expired | 20 | #24966 change choreography (stripped) |
| 82 | primitives | search | filter chips selectable removable tag group | 20 | #22213 on native checkboxes |
| 83 | primitives | search | notification count badge animated number | 15 | neutral real count |
| 84 | primitives | search | interactive navigation card hover arrow link card premium | 20 | #15606 underline wipe + diagonal arrow |
| 85 | primitives | search | document card file card status metadata actions | 20 | #28524 anatomy + #28271 vocabulary + #26871 silhouette (case file only) |
| 86 | primitives | search | feature card premium icon title description | 20 | #26797 hairline editorial grid |
| 87 | primitives | search | media card image editorial article card hover zoom | 15 | none directly (see #42) |
| 88 | primitives | search | course card learning module progress lessons | 15 | #19006 meter + #29442 next step |
| 89 | primitives | search | project card partnership initiative status milestone | 15 | #28524 + #28384 |
| 90 | primitives | search | profile card organization contact institution | 15 | #28632 with glyph discs |
| 91 | primitives | search | stat card KPI metric dashboard minimal | 15 | #4245 minimal |
| 92 | primitives | search | animated tabs | 20 | #23570 |
| 93 | primitives | search | segmented control | 20 | #753 native radios + #23552 thumb |
| 94 | primitives | search | tooltip popover | 20 | #23548 flip/clamp as JS fallback |
| 95 | primitives | search | dropdown menu actions icons shortcuts grouped destructive | 15 | coss/cnippet menu contract |
| 96 | primitives | search | modal premium | 11 | none (query biased to marketing → refined in #29) |
| 97 | primitives | search | drawer premium slide-over side sheet | 20 | #23558 behaviours |
| 98 | primitives | search | dialog modal accessible header footer actions becomes bottom sheet on mobile | 20 | #26905 |
| 99 | primitives | search | toast notification stacked accessible | 20 | #24297 stack + #26527 empty |
| 100 | primitives | search | notification center | 20 | #27135 doctrine + #28432 tabs |
| 101 | primitives | search | empty state professional | 20 | #19747 + contextual variants |
| 102 | primitives | search | skeleton shimmer | 20 | static skeleton + #29952 reveal |
| 103 | primitives | search | loader premium | 20 | → refined in #35 |
| 104 | primitives | search | loading spinner minimal elegant svg stroke draw logo loader | 20 | #16834 as reference for the door |
| 105 | primitives | search | pagination | 15 | server-side ellipsis pagination |
| 106 | primitives | get_inspiration | premium signature call-to-action, institutional legal-tech hero, dark navy, restrained metallic light, accessible | 12 | confirms #29293 |
| 107 | primitives | get_inspiration | status badge system for legal document review states, icon + label, animated state change, not colour-only | 12 | confirms #11/#12 |
| 108 | primitives | search | spotlight card border gradient follows pointer | 15 | border light without blur |
| 109 | primitives | search | button arrow icon slides on hover call to action | 15 | V4 arrow +3 px |
| 110 | primitives | search | official seal stamp badge certified verified authority | 12 | none — keep V3 `chip--seal` |
| 111 | primitives | search | image card with caption overlay gradient editorial news card | 15 | #28557 + #28132 |
| 112 | forms-docs | search | file upload premium | 30 | 27137 |
| 113 | forms-docs | search | attachment upload | 30 | 28271, 17767 (idea) |
| 114 | forms-docs | search | document management card | 30 | 28524, 25312 |
| 115 | forms-docs | search | data table premium | 30 | feeds C15 |
| 116 | forms-docs | search | advanced table | 30 | 23561 |
| 117 | forms-docs | search | filters bar | 30 | 26793, 518, 23525 |
| 118 | forms-docs | search | form input premium | 30 | 28301, 127 |
| 119 | forms-docs | search | sign in form fields | 30 | 21491 |
| 120 | forms-docs | search | document preview panel pdf viewer side drawer | 20 | 23558 |
| 121 | forms-docs | search | file list row with version history and status | 20 | 28496, 25163 |
| 122 | forms-docs | search | documents signing | 10 | 27137, 28871, 28857, 28828, 27135 |
| 123 | forms-docs | search | document card with status badge file type and actions | 20 | feeds C11 |
| 124 | forms-docs | search | expandable rows table sticky header row actions | 20 | 23696, 16937 (idea) |
| 125 | forms-docs | search | select dropdown native styled | 20 | 31494, 262 |
| 126 | forms-docs | search | textarea with character count and helper text | 15 | 29430, 190 |
| 127 | forms-docs | search | checkbox group consent terms | 15 | 24975, 661 |
| 128 | forms-docs | search | radio group cards with description selectable | 15 | 28339, 747 |
| 129 | forms-docs | search | switch toggle settings row label description | 15 | 25090, 26523 |
| 130 | forms-docs | search | slider discrete steps labels scale | 12 | none (route D) |
| 131 | forms-docs | search | segmented control filter with counts | 15 | 23552, 23525 |
| 132 | forms-docs | search | form validation error summary accessible | 12 | 333 (+28301) |
| 133 | forms-docs | search | file manager workspace dashboard documents sidebar | 20 | none as a whole |
| 134 | forms-docs | get_inspiration | legal case file upload: drag and drop, real progress, errors, retry, versions | 12 | 27137 confirmed top (confidence 0.57) |
| 135 | forms-docs | get_inspiration | institutional staff back-office data table | 12 | 19793 |
| 136 | forms-docs | search | document checklist required items status grouped sections | 20 | 24864 (partial), 23569 (idea) |
| 137 | forms-docs | search | inbox list grouped by section with counts and empty state | 20 | 29345 |
| 138 | forms-docs | search | application status tracker required documents progress | 15 | 29469 (partial) |
| 139 | forms-docs | search | error alert banner with list of field links | 12 | 29338 |
| 140 | platform-domains | search | modern animated sign in | 30 | Split Login #28369 (layout) |
| 141 | platform-domains | search | premium authentication split | 30 | #28369 |
| 142 | platform-domains | search | sign in split screen | 30 | #9106 (photo panel idea) |
| 143 | platform-domains | search | login page with editorial image panel and quote | 20 | — (confirms #28369 + #9106 combination) |
| 144 | platform-domains | search | authentication card | 20 | #28480 (reset sub-page anatomy) |
| 145 | platform-domains | get_inspiration | institutional legal-tech sign-in … no social login | 12 | #28369 confirmed top |
| 146 | platform-domains | search | dashboard premium | 30 | #14941 (shell qualities only) |
| 147 | platform-domains | search | dashboard greeting next step hero card workspace home | 20 | #19068 (image-band principle) |
| 148 | platform-domains | search | bento grid dashboard workspace | 15 | none |
| 149 | platform-domains | search | skeleton loading dashboard | 12 | #23557 (policy) + #29863 (shapes) |
| 150 | platform-domains | search | quick actions | 30 | #28284 |
| 151 | platform-domains | search | command palette *(also run by another lane)* | 15 | #23522 (P2, optional) |
| 152 | platform-domains | search | case management record detail page with inspector sidebar | 20 | #31745 (section index) |
| 153 | platform-domains | search | document checklist status required files | 20 | #30552 (tick micro-motion) + #28271 (file lifecycle) |
| 154 | platform-domains | search | activity timeline audit log | 20 | #28295 + #28483 + #29371 |
| 155 | platform-domains | search | timeline progress journey | 30 | #28273 (one image per step) |
| 156 | platform-domains | search | process stepper motion | 30 | #24556 + #24528 (Motion's own techniques) |
| 157 | platform-domains | search | scroll timeline vertical line draws on scroll | 20 | #857 (scroll-linked beam principle) |
| 158 | platform-domains | search | roadmap milestone path journey steps | 20 | #28384 (vertical / descriptive variant) |
| 159 | platform-domains | search | animated beam connecting two nodes svg path | 15 | #1149 (partial: beam on an SVG path) |
| 160 | platform-domains | get_inspiration | case journey progress rail … two jurisdictions | 12 | confirms #28384 |
| 161 | platform-domains | search | course card progress | 30 | #8698 (dashboard), #28524 (enrolment row) |
| 162 | platform-domains | search | course curriculum lesson list learning progress | 20 | #29458 (lesson list) |
| 163 | platform-domains | search | kanban project workspace | 30 | #29494 + #1400 (no drag) |
| 164 | platform-domains | search | discussion forum thread proposal voting governance | 20 | #26900 (partial) |
| 165 | platform-domains | search | support ticket helpdesk | 12 | #26714 + #24438 |
| 166 | platform-domains | search | inbox message thread conversation list | 20 | #28568 |
| 167 | platform-domains | search | ticket list table status priority assignee | 15 | #22187 (company table anatomy) |
| 168 | platform-domains | search | company dashboard | 30 | none as a whole (table anatomy from #22187) |
| 169 | platform-domains | search | segmented meter status health bar | 12 | none (ILE's notched meter is already better) |
| 170 | motion | search | border beam / light running a border *(query strings summarised in MOTION §14.6; exact strings not recorded there)* | — | #1268 (idea A, technique D) |
| 171 | motion | search | loaders — «counter loader», «Vault Lock», spinners, «Styled Progress Bars» *(query strings summarised in MOTION §14.6; exact strings not recorded there)* | — | — (all D) |
| 172 | motion | search | scroll-filled timelines — «Scroll Progress», «Growth Story Timeline», «Animated Roadmap», «Product Timeline» *(query strings summarised in MOTION §14.6; exact strings not recorded there)* | — | principle only (native scroll-driven CSS) |
| 173 | motion | search | progress stepper / border beam panel *(query strings summarised in MOTION §14.6; exact strings not recorded there)* | — | #28558 (line by scaleX), #23408 (radial mask detail) |
| 174 | mobile | search | mobile full screen hero … *(truncated in MOBILE_UX §1.4)* | — | #26796 «Hero 12» (principle A: copy anchored low; motion D) |
| 175 | mobile | search | sticky bottom action bar mobile … *(truncated in MOBILE_UX §1.4)* | — | — (floating action buttons, D) |

## 3. Code retrieved with `get_component` — 97 calls, 89 distinct components

| 21st id | Name (author) | Retrieved by | What the code taught (short) |
|---|---|---|---|
| #75 | Interactive Bento Gallery (anurag-mishra22) | hero-public | interactive bento gallery (rejected) |
| #393 | Dropdown Menu (profile with avatar) (originui) | nav-shell | account menu anatomy, keyboard-only focus return |
| #857 | Timeline (Aceternity) (manuarora700) | platform-domains | scroll-bound beam → CSS view timeline |
| #969 | Interactive Hover Button (dillionverma) | primitives | label read twice by AT (rejected) |
| #1268 | Border Beam (Magic UI) (magicui) | motion | offset-path border beam (not composited) |
| #1652 | Spotlight (border only) (ibelick) | primitives | blurred blob following the mouse (idea rewritten as border light) |
| #2034 | Modern Animated Sign In (arunachalam) | platform-domains | Next-only, logos, wipes (rejected) |
| #2061 | Smooth Scroll Hero (ishamsu) | hero-public | clip-path photo opening with scroll (rejected for the hero) |
| #8698 | ProjectProgressCard (ruixen.ui) | platform-domains | next-step card anatomy (from opacity 0 on load: rejected) |
| #9106 | Login — Auth Form Split Screen (lavikatiyar) | platform-domains | photo panel with bottom scrim (form animated from 0: rejected) |
| #9993 | Halide Topo Hero (shivendra9795kumar) | hero-public | topographic hero (rejected) |
| #10443 | Liquid Metal Button (johuniq) | primitives | paper-shaders liquid metal: injected `<style>`, fixed size, mouse-only |
| #10905 | Reveal Image Mask (daiwiikharihar) | hero-public | mask-bloom reveal |
| #11356 | coss Badge (coss.com) | primitives | badge anatomy, 8 % tint, coarse-pointer hit area |
| #14941 | Dashboard Sidebar (arunjdass) | platform-domains | rail palette discipline; div-onClick items (semantics rebuilt) |
| #16730 | Animated Banner (dqnamo) | hero-public | banner with photo overlay (poster variant) |
| #16834 | Logo Trace Loader (dqnamo) | nav-shell, primitives ×2 | logo trace loader; inline `<style>` in SVG — reference only |
| #17448 | Reshaped Badge (reshaped) | primitives | imports a whole design-system bundle (rejected) |
| #17767 | Reshaped File upload (reshaped) | forms-docs | dropzone holding the real input |
| #18041 | Scroll 01 (felipemenezes098) | hero-public | sticky figure answering the text |
| #18113 | Table of Contents (hirael) | nav-shell | TOC semantics; its «marker» was only a border swap |
| #18131 | Shop Navigation Menu (bundui) | nav-shell | — |
| #18149 | Page Header with Breadcrumbs (7ovr) | nav-shell | page header anatomy |
| #19009 | Sidebar Dashboard Skeleton (cnippet-dev) | nav-shell | full-shell skeleton (dropped: shell is server-rendered) |
| #19050 | Sign In Split Screen (felipemenezes098) | platform-domains | split screen with social proof (rejected) |
| #19077 | Editorial Image Hero (felipemenezes098) | hero-public | editorial image hero, mask fade |
| #19153 | Hero Liquid Metal (cult-ui) | hero-public | liquid-metal hero (WebGL, rejected) |
| #19747 | Empty (cnippet-dev) | primitives | fanned icon tiles (rejected as ILE signature) |
| #19793 | Table (cnippet-dev) | forms-docs | dependency-free semantic table |
| #21349 | Motion Navigation Menu (unlumen) | nav-shell | direction-aware content swap (opens on focus: 1.4.13 risk) |
| #21517 | Animated Sidebar (unlumen) | nav-shell | one travelling hover plate; dims others to 30 % (rejected) |
| #21563 | Liquid Metal (metal-fx) (larsen66) | primitives | metal-fx: 100.6 KB gz with react-dom |
| #22169 | Expanding Sub-Rows Table (felipemenezes098) | forms-docs | expandable table row (fixed ARIA) |
| #22313 | Drilldown Menu (ruixen.ui) | nav-shell | pinned drill-down row; per-character animation breaks Arabic (rejected) |
| #23408 | Border Beam Panel (Motiq) | motion | rAF-driven conic comets (CSP, repaint: rejected) |
| #23536 | Loading Button (ddoemonn) | primitives | stacked-faces state cell, single live region |
| #23541 | Pagination (ddoemonn) | primitives | pagination = Django get_elided_page_range |
| #23548 | Popover (ddoemonn) | primitives | popover flip/clamp fallback |
| #23552 | Segmented Control (ddoemonn) | forms-docs, nav-shell, primitives ×3 | segmented thumb with inverted labels; arrows not RTL-aware |
| #23557 | Skeleton Swap (ddoemonn) | nav-shell, platform-domains ×2 | skeleton delay / min-visible, reserved box, aria-busy |
| #23558 | Drawer (ddoemonn) | forms-docs, nav-shell, primitives ×3 | inert siblings, scroll lock with gutter compensation, SR hint |
| #23561 | Sortable Table (ddoemonn) | forms-docs | sortable th with aria-sort, stable sort |
| #23562 | Sticky Header (ddoemonn) | nav-shell | condensing sticky title |
| #23569 | Task Steps (ddoemonn) | forms-docs | task steps |
| #23570 | Tabs (ddoemonn) | primitives | tabs: roving tabindex, invisible bold sizer |
| #24297 | Toast (cnippet-dev) | primitives | toast stack via CSS variables |
| #24379 | Ocean grain (hazelgrace3026) | hero-public | pure-CSS silk gradient + SVG grain |
| #24399 | Aceternity Button (saurabh-2607) | primitives | 1 px inner light; outline removed without replacement |
| #24556 | Along path † (motiondotdev) | platform-domains | offset-path marker (not composited in Chrome 153) |
| #24864 | Onboarding Step Tracker (cnippet-dev) | forms-docs | count line under the title |
| #24966 | Multi state badge (motiondotdev) | primitives | multi-state badge choreography (stripped of blur, shake, scale) |
| #25501 | Gradient CTA Button (mengto) | primitives | layered inset lighting |
| #26531 | Metal Button (arihantcodes_1f7b8c4d) | primitives | metal-fx wrapper, focus outline hidden |
| #26656 | FAQ Two Column (hirael) | hero-public | two-column FAQ frame |
| #26796 | Hero 12 (—) | mobile | copy anchored to the bottom of an image hero (principle kept) |
| #26797 | Feature Grid Spotlight Cards (hirael) | hero-public, primitives ×2 | spotlight via --mx/--my; hairline grid |
| #26824 | Filter Token Bar (laziekiki) | forms-docs | filter token bar |
| #26871 | Folder Card (uvain) | primitives | folder silhouette (rejected) |
| #26905 | Animated Dialog (rmahammad) | primitives | dialog: pinned header/footer, ζ ≈ .93 spring, forced-colours close |
| #26923 | Segmented Tabs (micka_design) | primitives | animates left/top/width (rejected) |
| #27010 | Hover Expand Gallery (kedhareswer) | hero-public | hover-expand gallery (flex-grow → CLS, rejected) |
| #27093 | Filmstrip Gallery (n1m4mz) | hero-public | filmstrip gallery + native dialog lightbox |
| #27135 | Notification Panel (uvain) | primitives | sentence-first notification rows (nested interactive, fixed in V5) |
| #27137 | File Upload (uvain) | forms-docs | upload: client guards, retry, drag depth, abort |
| #27378 | Command Menu with Global Search (ephraimduncan) | nav-shell | recents + type filters; «Personnes» (rejected) |
| #27428 | Morphing Scroll Navbar (laziekiki) | nav-shell | scroll states letterhead → compact bar (overshoot curve removed) |
| #27897 | Mobile Navigation Tabs (shadcnui-blocks) | nav-shell | glyph + label always visible bottom bar |
| #28271 | Attachment States (uiable) | forms-docs | attachment lifecycle states |
| #28273 | Growth Story Timeline (shadcnspace) | hero-public | timeline with a photo per step (core file not returned) |
| #28295 | Timeline (cubby-ui) (cubby-ui) | platform-domains | timeline state model with <time> |
| #28301 | Field Validation (ai2) | forms-docs | field state model with aria-describedby |
| #28369 | Split Login (hirael) | platform-domains | split login, form without card, serif H1 (infinite loops removed) |
| #28496 | File List Item (felipemenezes098) | forms-docs | file meta line «PDF · 1,2 Mo · version 3» |
| #28558 | Animated Progress Stepper (shadcnspace) | motion, platform-domains ×2 | scaleX progress line; left animation and pulse rejected |
| #29229 | Breadcrumb with Folder Menu (coss.com) | nav-shell | breadcrumb collapse to «…» |
| #29293 | Metallic Button (starc007) | primitives | chrome rim + inset surface |
| #29334 | Animated Sidebar (starc007) | nav-shell | rail ↔ sidebar focus model, inert, focus return |
| #29338 | Destructive Alert with Action List (sean0205) | forms-docs | destructive alert with action list |
| #29371 | Processing Timeline (rmahammad) | platform-domains | status vocabulary, «never fake a status» |
| #29773 | Footer with Suite (scrollxui) | hero-public | footer closing band |
| #29952 | Skeleton Reveal (arihantcodes_1f7b8c4d) | primitives | skeleton reveal (blur removed) |
| #29954 | Tree Nav (arihantcodes_1f7b8c4d) | nav-shell | critically damped marker glide, logical properties |
| #29989 | Search Empty State (arihantcodes_1f7b8c4d) | nav-shell | zero-result suggestions |
| #30552 | Onboarding Checklist (ssychui) | platform-domains | fill-then-tick sequencing |
| #30554 | Project Index (ssychui) | hero-public | project index keyboard parity |
| #31184 | Morphing Search (starc007) | nav-shell | search button morphing into a field |
| #31494 | Native Select (wensity) | forms-docs | native select styled |
| #31509 | Navigation Menu (wensity) | nav-shell | complete keyboard model, hover-intent delays, viewport morph |
| #31723 | Mega Menu Navbar (anelkabag) | nav-shell | bar and panel as one surface |

## 4. Compliance statement

- **Allowed tools only:** `search`, `get_inspiration`, `get_component`, `get_usage` (tier check). **Never called:** `generate`, `iterate_generation` (0 in every lane, as each lane's report states). **This is a declaration, not a verification** (`RED_TEAM` m18): no role can read a call history from the 21st account — `get_usage` reports the tier's entitlement, not the calls made — and this role made no 21st call, in the first pass or in the red-team revision.
- **No 21st asset at runtime:** preview images were downloaded only for internal review into `captures/21st_*` and `scratch/21st_*` and are not licensed for the product; nothing from `cdn.21st.dev` is referenced by any proposal; no code was copied.
- **Known gaps:** preview videos not watched; several candidates judged on metadata only (marked † in the hero register); `get_component` for #28273 did not return its core file; result counts are approximate (not deduplicated by the curators).
