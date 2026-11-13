/**
 * The home hero, design V5.4 — the final version (docs/design-v5/V5_4_EXECUTION_PLAN.md §1.17; DL54-06; HERO_FINAL.md and
 * the Creative Director's decision). W2-D's port of the proof's he.js (C:/tmp/ile_v5_council/proof/research/hero/he/):
 * one module, no library, no frame loop, CSP-clean — no inline style, no injected <style>, no eval. Its one import is the
 * motion gate (static/js/src/motion.js, W1-D; plan §1.5): whether the page may move is asked there — reducedMotion(), the
 * person's setting or the preview's html.rm — and every element.animate() and every frame wait passes through its play(),
 * nextFrame() and afterPaint() (tests/frontend/test_script_motion_gate.py). Every light
 * is an element that already exists (templates/pages/home/_hero.html), moved with the Web Animations API on transform and
 * opacity only. Nothing here is needed to read or to use the page: without this module the hero is its rested picture (the
 * door closed), and colour, the call, the route and the door's answer follow the hand by CSS alone (hero.css).
 *
 * The layers (HERO_FINAL_BRIEF §10):
 *   REST         the first paint is the whole message (the stage as the owner drew it, closed, with the lit steps).
 *   AMBIENT      none: nothing loops, nothing drifts (WCAG 2.2.2 has nothing to pause).
 *   DISCOVERY    once per session (CD ruling R6), after the largest paint, the door decoded, the hero in view, an idle slot
 *                and --motion-wait. Desktop (≈ 3.5 s at 1440 × 900): 1 the four are NAMED (their photographs turn to colour,
 *                100 ms apart) → 2 they FEED THE PATH (a light rises up each stem) → 3 THE PATH (the origin's shore glints,
 *                a bead of light with a long warm glow glides along the inlay — the inlay staying lit behind it until the
 *                doorway takes the light, never an ink fill —, each station's ring glints as it passes; past the reveal gold
 *                light, landing on the terminal disc) → 4 THE DOORWAY (the arch light from the springing; the threshold lit)
 *                → 5 THE STEPS (bottom → top) → 6 THE KEY turns (rotateY 0 → 360° in 800 ms on the hero's --he-ease-turn,
 *                a warm halo behind it and a glint as its face returns: it passes its mirror image and ends on the verbatim
 *                key, DL54-08) → 7 THE DOOR OPENS (a band of warm light at the leaf's edge, the spill on the steps) → 8 THE
 *                FOUR TOGETHER (the door's light lifts the four at once) → 9 SETTLE (black-and-white again; the door stays
 *                ajar, DL54-11 — the last pixel to stop moving is the door's light). Phone (≈ 2.8 s): named → the spine →
 *                the rail, its corner and the floor run to the first step → steps → key → the door opens → together →
 *                settle. Any interruption (a press, a key, the hero out of view, a hidden tab, a breakpoint) lands on the
 *                settled still in --motion-fast; the key never turns back (it lands forward at the turn's own pace).
 *   INTERACTION  CSS (hero.css); here: the hand wins over the score on its origin, the press state (.is-pressed, so that
 *                WebKit shows it too), the keyboard modality (html.he-keys: every state at 0 ms both ways), the
 *                view-transition names at a press — and THE REPEATABLE FLOW (the owner's V5.5 directive): on the settled
 *                hero, a hover with a fine pointer or a touch on an origin runs the light along the one path to the door
 *                again, every time — the shore's glint, the inlay's light, the gold run, the arch light, the steps — shorter
 *                than the discovery (≈ 1.3 s), cancelled where it stands when the hand leaves — and from the keyboard too
 *                (the review fix): focus on an origin runs its light, its states still instant; a button over the golden
 *                key (.he-replay) replays the whole sequence on Enter, Space or a click. Never under reduced motion or
 *                forced colours, never while the discovery plays. The key does not turn under the hand (D8).
 *                A FINGER'S PRESS WAITS (the review's M2): the press state and the light are armed 100 ms after the finger
 *                lands, or when it lifts sooner — a scroll that starts on a tile is cancelled by the browser before that
 *                and shows nothing —, and a tap keeps them while the next page answers. WHERE NOTHING HOVERS (the review's
 *                M4) the same short light runs once each time the hero comes back into view after having left it.
 *   TRANSITION   view-transition-ready names on the pressed origin.
 * Reduced motion and forced colours: the settled still, at once; nothing plays, nothing flows (the tokens zero the CSS
 * transitions). The probes read data-he-clock on the hero and data-he-error on <html>.
 */

import { afterPaint, durationToken, nextFrame, play as throughGate, reducedMotion } from './motion.js';

const root = document.documentElement;
const hero = document.querySelector('[data-he]');

document.addEventListener('keydown', (e) => { if (!e.metaKey && !e.ctrlKey && !e.altKey) root.classList.add('he-keys'); }, { capture: true, passive: true });
const pointerMode = () => { if (root.classList.contains('he-keys')) root.classList.remove('he-keys'); };
document.addEventListener('pointerdown', pointerMode, { capture: true, passive: true });
document.addEventListener('pointermove', pointerMode, { capture: true, passive: true });

const mqForced = window.matchMedia('(forced-colors: active)');
const mqHover = window.matchMedia('(hover: hover) and (pointer: fine)');
const mqTouch = window.matchMedia('(hover: none)');   // a screen where nothing hovers
const mqDesk = window.matchMedia('(min-width: 64rem)');
const mqWide = window.matchMedia('(min-width: 80rem)');
const mqLand = window.matchMedia('(max-width: 63.999rem) and (min-width: 36rem) and (orientation: landscape) and (max-height: 30rem)');
const stillPage = () => reducedMotion() || mqForced.matches;   // the gate (the setting, or the preview's html.rm), and forced colours
const SEEN_KEY = 'ile.hero.discovered';   // sessionStorage: once per session, a per-visitor convenience; nothing sent

// durations and curves are read from the tokens — the durations through the gate's durationToken(), with their unit (a minified
// sheet writes 120ms as .12s)
const tokMs = (n, d) => { const v = durationToken(n, d); return Number.isFinite(v) && v > 0 ? v : d; };
const tokStr = (n, d, el = root) => (getComputedStyle(el).getPropertyValue(n).trim() || d);
const T = { fast: tokMs('--motion-fast', 120), standard: tokMs('--motion-standard', 200), slow: tokMs('--motion-slow', 480),
  wait: tokMs('--motion-wait', 400), stagger: tokMs('--motion-stagger', 60), spring: tokMs('--spring-soft-duration', 430) };
const ENTER = tokStr('--ease-enter', 'ease-out');
const EXIT = tokStr('--ease-exit', 'ease-in-out');
const SINE = tokStr('--ease-sine', 'ease-in-out');
const SPRING = tokStr('--spring-soft', 'ease-out');
const TURN = tokStr('--he-ease-turn', tokStr('--ease-turn', 'cubic-bezier(0.77, 0, 0.175, 1)'));   // the hero's own turn curve (tokens §4.2, motion M-B); the loader keeps --ease-turn
function lengthPx(el, name) {
  const raw = getComputedStyle(el).getPropertyValue(name).trim();
  const v = parseFloat(raw);
  if (!Number.isFinite(v)) return 0;
  if (raw.endsWith('rem')) return v * (parseFloat(getComputedStyle(root).fontSize) || 16);
  if (raw.endsWith('em')) return v * (parseFloat(getComputedStyle(el).fontSize) || 16);
  return v;
}

const $ = (sel, scope = hero) => scope.querySelector(sel);
const $$ = (sel, scope = hero) => Array.from(scope.querySelectorAll(sel));
const drawn = (el) => !!el && (el.offsetWidth > 0 || el.offsetHeight > 0);   // display: none → 0 × 0
const clamp = (lo, x, hi) => Math.min(hi, Math.max(lo, x));
const cancel = (a) => { try { a.cancel(); } catch (e) { /* already gone */ } };

let running = [];              // the discovery's animations
let discovering = false;
let letGoAt = -1e9;            // when the last interruption landed (a press on the replay during the movement is an interruption, not a replay)
let run = 0;                   // the discovery's generation: a stale promise never touches a newer run
let clockEnd = 0;              // the one clock's length (the discovery's, or the flow's while it plays)
const scripted = new Map();    // origin key → its scripted animations (the hand cancels them)
let letGoHandlers = [];

/* ---- one clock (G8): every animation starts with the clock and ends with it; its window lives in the offsets. The window
   must be finite and positive; the offsets are a running maximum clamped into [a, b] ---- */
function offsetsOf(frames) {
  const n = frames.length;
  let prev = 0;
  return frames.map((f, k) => {
    const raw = f.offset ?? (n > 1 ? k / (n - 1) : 0);
    const o = Math.min(1, Math.max(prev, Number.isFinite(raw) ? raw : prev));
    prev = o;
    return o;
  });
}
function play(el, frames, start, duration, outside = {}) {
  if (!el || !frames.length || !Number.isFinite(start) || !Number.isFinite(duration) || !(duration > 0)) return null;
  const end = clockEnd;
  if (!Number.isFinite(end) || !(end > 0)) return null;
  const offs = offsetsOf(frames);
  const a = Math.max(0, Math.min(1, start / end));
  const b = Math.max(a, Math.min(1, (start + duration) / end));
  if (!(b > a)) return null;
  let prev = a;
  const local = frames.map((f, k) => { const o = Math.min(b, Math.max(prev, a + offs[k] * (b - a))); prev = o; return { ...f, offset: o }; });
  const strip = ({ offset, easing, ...rest }) => rest;
  const before = { ...strip(frames[0]), ...outside.before }, after = { ...strip(frames[frames.length - 1]), ...outside.after };
  return throughGate(el, [{ ...before, offset: 0 }, { ...before, offset: a }, ...local, { ...after, offset: b }, { ...after, offset: 1 }],
    { duration: end, fill: 'none', easing: 'linear' });
}
/* a value that rises at `on` (in `up` ms), holds, and falls from `off` (in `down` ms) */
function hold(el, prop, on, up, off, down, peak, base, upEase, downEase, extra = {}) {
  const span = off + down - on;
  if (!el || !(span > 0) || !(up > 0) || !(down > 0)) return null;
  const v = (x) => ({ [prop]: x, ...extra });
  return play(el, [
    { ...v(base), offset: 0, easing: upEase },
    { ...v(peak), offset: up / span },
    { ...v(peak), offset: Math.max(up, off - on) / span, easing: downEase },
    { ...v(base), offset: 1 },
  ], on, span, { before: v(base), after: v(base) });
}

function modeOf() { return mqDesk.matches ? (mqWide.matches ? 'desk' : 'compact') : (mqLand.matches ? 'land' : 'phone'); }

/* ---- the kit: the reads and the moves shared by the discovery and the hand's flow (every read before any class flip) ---- */
function kit() {
  const rtl = getComputedStyle(hero).direction === 'rtl';
  const dir = rtl ? -1 : 1;
  const H = lengthPx(hero, '--head') || 24;
  const origins = $$('[data-origin]');
  const stations = $$('[data-station]');
  const litOf = (i) => stations[i] && $('.he-station__lit', stations[i]);
  const door = {
    ring: $('[data-arch="ring"]'), streak: $('[data-arch="streak"]'), key: $('.door-stage__key > .kg'),
    keyHalo: $('[data-key-halo]'), keyGlint: $('[data-key-glint]'),
    band: $('[data-aperture]'), spill: $('[data-spill]'), bloom: $('[data-bloom]'), treads: [3, 2, 1].map((n) => $(`[data-tread="${n}"]`)),   // bottom → top
  };
  const tx = (px) => `translateX(${dir * px}px)`;
  const ty = (px) => `translateY(${px}px)`;
  const clip = (sel) => { const w = $(sel); if (!drawn(w)) return null; const bar = $('.he-wipe__bar', w); return { el: bar, box: w, w: w.offsetWidth, h: w.offsetHeight, bw: bar ? bar.offsetWidth : 0, r: w.getBoundingClientRect() }; };
  const along = (r, el) => {   // a node's centre along a horizontal clip, from its reading start
    const n = el.getBoundingClientRect(); const c = n.left + n.width / 2;
    return rtl ? r.right - c : c - r.left;
  };
  // a horizontal wipe: the bar (its length + the head) slides from outside its clip to cover it; the head leads, the trace stays
  const wipeH = (c, start, v, off) => {
    if (!c || !(c.w > 0) || !(v > 0)) return null;
    const travel = (c.w + H) / v;
    return play(c.el, [
      { transform: tx(-(c.w + H)), opacity: 1, offset: 0 },
      { transform: tx(0), opacity: 1, offset: travel / (off + T.slow - start) },
      { transform: tx(0), opacity: 1, offset: (off - start) / (off + T.slow - start), easing: ENTER },
      { transform: tx(0), opacity: 0, offset: 1 },
    ], start, off + T.slow - start, { before: { transform: tx(-(c.w + H)), opacity: 0 }, after: { transform: tx(0), opacity: 0 } });
  };
  // a station's glint: the ring lights as the light passes and goes back to rest (from scale .85, never from 0)
  const glint = (el, at, up, down) => el && play(el, [
    { transform: 'scale(0.85)', opacity: 0, offset: 0, easing: ENTER },
    { transform: 'scale(1)', opacity: 1, offset: up / (up + down), easing: ENTER },
    { transform: 'scale(1)', opacity: 0, offset: 1 },
  ], at, up + down, { before: { transform: 'scale(0.85)', opacity: 0 }, after: { transform: 'scale(1)', opacity: 0 } });
  // a vertical wipe, upward (from its bottom) or downward (from its top)
  const wipeV = (c, start, v, off, up) => {
    if (!c || !(c.h > 0) || !(v > 0)) return null;
    const L = c.h + H, travel = L / v, from = up ? ty(L) : ty(-L);
    return play(c.el, [
      { transform: from, opacity: 1, offset: 0 },
      { transform: ty(0), opacity: 1, offset: travel / (off + T.slow - start) },
      { transform: ty(0), opacity: 1, offset: (off - start) / (off + T.slow - start), easing: ENTER },
      { transform: ty(0), opacity: 0, offset: 1 },
    ], start, off + T.slow - start, { before: { transform: from, opacity: 0 }, after: { transform: ty(0), opacity: 0 } });
  };
  const ring = (el, at, off, up = 160) => el && play(el, [   // a station's ring fills as the light passes (from scale .85)
    { transform: 'scale(0.85)', opacity: 0, offset: 0, easing: ENTER },
    { transform: 'scale(1)', opacity: 1, offset: up / (off + T.slow - at) },
    { transform: 'scale(1)', opacity: 1, offset: Math.max(up, off - at) / (off + T.slow - at), easing: ENTER },
    { transform: 'scale(1)', opacity: 0, offset: 1 },
  ], at, off + T.slow - at, { before: { transform: 'scale(0.85)', opacity: 0 }, after: { transform: 'scale(1)', opacity: 0 } });
  // the arch light: the ring over the arch (RTL: mirrored, from the right springing), then the streak down the far jamb
  const rot = (deg) => `scaleX(${dir}) rotate(${deg}deg)`;
  const archLight = (later, at) => {
    later(2, () => door.ring && play(door.ring, [{ transform: rot(0), opacity: 1, offset: 0, easing: SINE }, { transform: rot(239.396), opacity: 1, offset: 1 }],
      at, 275, { before: { transform: rot(0), opacity: 0 }, after: { transform: rot(239.396), opacity: 0 } }));
    later(2, () => door.streak && play(door.streak, [{ transform: 'translateY(-100%)', opacity: 1, offset: 0, easing: ENTER }, { transform: 'translateY(160.975%)', opacity: 1, offset: 1 }],
      at + 240, 260, { before: { transform: 'translateY(-100%)', opacity: 0 }, after: { transform: 'translateY(160.975%)', opacity: 0 } }));
  };
  return { rtl, dir, H, origins, stations, litOf, door, tx, ty, clip, along, wipeH, glint, wipeV, ring, archLight };
}

/* ---- the plan: every read and every keyframe computed now, in the idle slot, before the class flip; the animate() calls are
   closures issued over two frames on one start time (batch 1: the origins and the lines; batch 2: the stations and the door) ---- */
function buildDiscovery(mode) {
  const ops = [];
  const later = (batch, fn, key) => ops.push({ batch, fn, key });
  const k = kit();
  const { H, origins, stations, litOf, door } = k;
  const keyOf = (li) => li.dataset.aud;
  const phone = mode === 'phone', land = mode === 'land', compact = mode === 'compact';
  const named = origins.map((li, n) => (phone || land ? n * T.stagger : n * 100));
  let T0;                    // the light reaches the door (the springing on the desktop, the first step on a phone)
  const plan = { mode, named: named.map(Math.round) };

  if (mode === 'desk' || compact) {
    // 2 · they feed the path — desk: each stem lit upward from its eyelet; compact: the string lit row by row, bottom → top
    let pathStart = 520;
    const feeds = [];
    if (compact) {
      const segs = origins.map((li) => $('.he-origin__stem', li)).map((el) => (drawn(el) ? { el, len: el.offsetHeight } : null));
      const vs = 0.62;
      let t = 60;
      for (let n = segs.length - 1; n >= 0; n -= 1) { const sg = segs[n]; if (!sg) continue; feeds[n] = { el: sg.el, at: t, dur: Math.max(60, sg.len / vs) }; t += sg.len / vs; }
      pathStart = t + 60;
      const corner = $('[data-corner="maroc"]');
      if (drawn(corner)) plan.corner = { el: corner, at: t };
    } else {
      origins.forEach((li, n) => { const el = $('.he-origin__stem', li); if (drawn(el)) feeds[n] = { el, at: 60 + 100 * n, dur: 180 }; });
    }
    const wall = k.clip('.he-wipe--wall'), night = k.clip('.he-wipe--night');
    const L = (wall ? wall.w : 0) + (night ? night.w : 0);
    const v = clamp(0.66, L / 930, 1.4);                 // ≈ 930 ms from the shore to the door on any wall from 1280 up (the wall takes the page: ≈ 900 px at 1440, ≈ 1 250 at 1920), so the clock keeps D3's length
    const tSeam = pathStart + (wall ? wall.w : 0) / v;
    T0 = tSeam + ((night ? night.w - 7.5 : 0) + H / 2) / v;   // the head on the terminal disc
    // the key turns for 800 ms (motion M-B) and the door opens as it lands; the four's lift (G) comes once the key's halo has gone,
    // so that no frame changes more than 10 % of the screen (D4's curtain); END ≈ 3.55 s at 1440 (D3: ≤ 3.6 s)
    const A = T0 + 940, G = T0 + 1400, S = T0 + 1500, END = S + 600;
    clockEnd = END;
    const off = S;           // the twins leave at the settle
    Object.assign(plan, { v: Math.round(v * 1000) / 1000, pathStart: Math.round(pathStart), springing: Math.round(T0), end: Math.round(END) });

    origins.forEach((li, n) => {
      const key = keyOf(li);
      // 1 · named: colour in 240 ms, held while their light travels, released when the light rests in the door (600 ms)
      later(1, () => hold($('.he-plate__col', li), 'opacity', named[n], 240, S, 600, 1, 0, ENTER, EXIT), key);
      const f = feeds[n];
      if (f) {   // the light rises up the stem (scaleY, linear), holds a beat, and the stem is bronze again (320 ms, ease-out)
        const span = f.dur + 80 + 320;
        later(1, () => play(f.el, [
          { transform: 'scaleY(0)', opacity: 1, offset: 0 },
          { transform: 'scaleY(1)', opacity: 1, offset: f.dur / span },
          { transform: 'scaleY(1)', opacity: 1, offset: (f.dur + 80) / span, easing: ENTER },
          { transform: 'scaleY(1)', opacity: 0, offset: 1 },
        ], f.at, span, { before: { transform: 'scaleY(0)', opacity: 0 }, after: { transform: 'scaleY(1)', opacity: 0 } }), key);
      }
      // 1 + 8 · the light on the photograph: arriving (a brief lift that leaves the colour), and the door's light reaching the four
      later(2, () => lifts($('.he-plate__veil', li), named[n], G, [120, 260], [120, 120, 200], 0.6, 0.42), key);   // .42: with the larger plates of the wide wall the four's lift keeps under D4's curtain (10 % of the screen by luma) at 1920 × 1080 too
      const eye = $('.he-origin__eye', li);
      if (drawn(eye)) later(2, () => hold(eye, 'opacity', G, 120, G + 240, 200, 1, 0, ENTER, EXIT), key);
    });
    if (plan.corner) { const c = plan.corner; later(1, () => hold(c.el, 'opacity', c.at, 60, c.at + 140, 320, 1, 0, 'linear', ENTER)); delete plan.corner; }
    // 3 · the path: the shore glints as the light leaves it; a warm light glides along the inlay; each ring glints as it passes;
    // past the reveal gold light that stays, landing on the disc
    later(1, () => k.wipeH(wall, pathStart, v, T0 + 400));   // the inlay stays lit behind the head until the doorway has taken the light (motion M-A)
    later(1, () => k.wipeH(night, tSeam, v, off));
    later(2, () => k.glint(litOf(0), pathStart, 160, 520));
    if (wall) [1, 2, 3, 4].forEach((i) => { const st = stations[i]; const node = st && $('.he-station__node', st); if (drawn(node)) later(2, () => k.glint(litOf(i), pathStart + (k.along(wall.r, node) + H / 2) / v - 40, 120, 440)); });
    // 4 · the doorway: the arch light from the springing; the threshold lit; the halo rises
    k.archLight(later, T0);
    later(2, () => hold($('[data-halo]'), 'opacity', T0, 450, A - 100, 400, 1, 0, ENTER, EXIT));   // down before the band peaks (motion m-6); the threshold itself is lit by the steps and the arch — its station draws no light of its own here (the review's m1)
    addDoor(later, door, { steps: T0 + 110, gap: 70, key: T0 + 300, keyDur: 800, treadsOff: A, haloHold: 100, haloFall: 400, A, S, END, band: T.spring, down: 600 });
  } else {
    // phones: the spine (up) and its junction, then the rail from the shore (down), its corner, the floor run to the first step
    const spine = k.clip('.he-wipe--spine'), rail = k.clip('.he-wipe--rail'), floor = k.clip('.he-wipe--floor');
    const junction = $('[data-junction]'), corner = $('[data-corner="rail"]');
    const sStart = 160, sDur = 240;
    const vS = spine ? (spine.h + H) / sDur : 1;
    const r0 = 380, cornerLen = 18.85;
    const Lr = (rail ? rail.h : 0) + (rail ? cornerLen : 0) + (floor ? floor.w : 0);
    const vR = clamp(0.5, Lr / 870, 1.2);              // a phone's route ≈ 0.5 px/ms; a tablet's longer route keeps the same duration
    const tCorner = r0 + (rail ? rail.h : 0) / vR;
    const tFloor = tCorner + (rail ? cornerLen : 0) / vR;
    T0 = land ? 300 : (floor ? tFloor + (floor.w + H / 2) / vR : tCorner + 60);
    // the key turns for 640 ms and the door opens in its last third (the phone's short clock: the door's beat must hold ≥ 4 % of the
    // screen for 600 ms before the settle takes it back, D4); END ≈ 2.75 s at 390 (D3: ≤ 2.8 s)
    const A = T0 + 560, G = T0 + 880, S = T0 + 1100, END = S + 400;
    clockEnd = END;
    const off = S;
    Object.assign(plan, { v: Math.round(vR * 1000) / 1000, firstStep: Math.round(T0), end: Math.round(END) });
    origins.forEach((li, n) => {
      const key = keyOf(li);
      later(1, () => hold($('.he-plate__col', li), 'opacity', named[n], 240, S, 460, 1, 0, ENTER, EXIT), key);
      later(2, () => lifts($('.he-plate__veil', li), named[n], G, [100, 240, 160], [100, 80, 120], 1, 0.37), key);   // the small chips need the stronger light
    });
    if (!land) {
      later(1, () => k.wipeV(spine, sStart, vS, off, true));
      if (drawn(junction)) later(1, () => hold(junction, 'opacity', sStart + sDur, T.fast, off, 400, 1, 0, ENTER, ENTER));
      later(1, () => k.wipeV(rail, r0, vR, off, false));
      if (drawn(corner)) later(1, () => hold(corner, 'opacity', tCorner, 40, off, 400, 1, 0, 'linear', ENTER));
      later(1, () => k.wipeH(floor, tFloor, vR, off));
      // the six nodes light as the rail's head passes (the shore first)
      if (rail) stations.forEach((st, i) => {
        const node = $('.he-station__node', st), lit = litOf(i);
        if (!drawn(node) || !lit) return;
        const n = node.getBoundingClientRect();
        const y = n.top + n.height / 2 - rail.r.top;
        later(2, () => k.ring(lit, r0 + Math.max(0, y + H / 2) / vR, off, 140));
      });
    }
    later(2, () => hold($('[data-halo]'), 'opacity', T0, 380, S + 100, 400, 1, 0, ENTER, EXIT));   // the light reaches the first step, then the doorway glows — held past the settle's start: the door's beat ≥ 4 % for ≥ 600 ms on a phone (motion M-C)
    addDoor(later, door, { steps: T0, gap: 70, key: T0 + 150, keyDur: 640, treadsOff: S, haloHold: 500, haloFall: 500, A, S, END, band: T.spring, down: 460 });
  }
  plan.animations = ops.length;
  return { ops, plan, end: clockEnd };
}

/* the photograph's veil: two lifts in one keyframe list — the light arriving at the naming [up, down] and the door's light
   reaching the four [up, hold, down] */
function lifts(el, at, g, a, b, p1, p2) {
  if (!el) return null;
  const end = g + b[0] + b[1] + b[2], span = end - at;
  if (!(span > 0) || at + a[0] + (a[2] || 0) + a[1] > g) return null;
  const o = (x) => (x - at) / span;
  return play(el, [
    { opacity: 0, offset: 0, easing: ENTER }, { opacity: p1, offset: o(at + a[0]) }, { opacity: p1, offset: o(at + a[0] + (a[2] || 0)), easing: EXIT }, { opacity: 0, offset: o(at + a[0] + (a[2] || 0) + a[1]) },
    { opacity: 0, offset: o(g), easing: ENTER }, { opacity: p2, offset: o(g + b[0]) }, { opacity: p2, offset: o(g + b[0] + b[1]), easing: EXIT }, { opacity: 0, offset: 1 },
  ], at, span, { before: { opacity: 0 }, after: { opacity: 0 } });
}

/* the door's beats, shared: 5 the steps light bottom → top, 6 the key turns once (rotateY 0 → 360° about its shaft on the hero's
   turn curve, 800 ms on the desktop — the half-turn ≈ 300 ms —, a warm halo behind it, a glint across the bow as its face returns;
   its last frame is the owner's key), 7 the door opens — the band slides in from the leaf's edge on the soft spring while its
   opacity reaches 1 in the first 40 %, the spill rises, the steps' twins hand over to it (t.treadsOff); 9 the band and the spill
   settle to their rest (0.9): the last pixels to stop moving */
function addDoor(later, d, t) {
  const { A, S, END } = t;
  d.treads.forEach((el, j) => { if (el) later(2, () => hold(el, 'opacity', t.steps + j * t.gap, 140, t.treadsOff || A, 480, 1, 0, ENTER, ENTER)); });
  later(2, () => d.key && play(d.key, [{ transform: 'rotateY(0deg)', offset: 0, easing: TURN }, { transform: 'rotateY(360deg)', offset: 1 }],
    t.key, t.keyDur, { before: { transform: 'rotateY(0deg)' }, after: { transform: 'rotateY(360deg)' } }));
  // the light response (motion M-B): the halo while the key turns; the glint as the face comes back (≈ 74 % of the turn on the hero's curve)
  later(2, () => d.keyHalo && hold(d.keyHalo, 'opacity', t.key, 280, t.key + t.keyDur + t.haloHold, t.haloFall, 0.9, 0, ENTER, EXIT));   // held past the landing: the unlock's light stays on the door while it opens (the door's beat, D4); longer on phones
  const glintAt = t.key + Math.round(t.keyDur * 0.74);
  later(2, () => d.keyGlint && hold(d.keyGlint, 'opacity', glintAt, 80, glintAt + 80, 200, 1, 0, ENTER, EXIT));
  const span = END - A;
  later(2, () => d.band && play(d.band, [
    { transform: 'translateX(100%)', opacity: 0, offset: 0, easing: SPRING },
    { opacity: 1, offset: (0.4 * t.band) / span },
    { transform: 'translateX(0%)', offset: t.band / span },
    { opacity: 1, offset: (S + 40 - A) / span, easing: EXIT },
    { transform: 'translateX(0%)', opacity: 0.9, offset: 1 },
  ], A, span, { before: { transform: 'translateX(100%)', opacity: 0 }, after: { transform: 'translateX(0%)', opacity: 0.9 } }));
  later(2, () => d.bloom && play(d.bloom, [   // the opening's light beside the leaf, with the band
    { opacity: 0, offset: 0, easing: ENTER },
    { opacity: 1, offset: (0.4 * t.band) / span },
    { opacity: 1, offset: (S + 40 - A) / span, easing: EXIT },
    { opacity: 0.9, offset: 1 },
  ], A, span, { before: { opacity: 0 }, after: { opacity: 0.9 } }));
  later(2, () => d.spill && play(d.spill, [
    { opacity: 0, offset: 0, easing: ENTER },
    { opacity: 1, offset: 480 / span },
    { opacity: 1, offset: (S + 40 - A) / span, easing: EXIT },
    { opacity: 0.9, offset: 1 },
  ], A, span, { before: { opacity: 0 }, after: { opacity: 0.9 } }));
}

/* issue one batch of the plan; every animation of the sequence on one start time (t0), so that two frames make one clock */
function issue(plan, batch, t0) {
  plan.ops.filter((op) => op.batch === batch).forEach((op) => {
    const made = op.fn();
    const list = (Array.isArray(made) ? made : [made]).filter(Boolean);
    list.forEach((a) => {
      if (t0 !== null && t0 !== undefined) { try { a.startTime = t0; } catch (e) { /* keeps its own start */ } }
      running.push(a);
      if (op.key) { if (!scripted.has(op.key)) scripted.set(op.key, []); scripted.get(op.key).push(a); }
    });
  });
}

function settle() {
  discovering = false;
  running = [];
  scripted.clear();
  hero.classList.remove('is-discovering', 'is-priming');
  hero.classList.add('is-ajar');                       // the settled hero: the door ajar
  letGoHandlers.forEach((off) => off());
  letGoHandlers = [];
  try { window.sessionStorage.setItem(SEEN_KEY, '1'); } catch (e) { /* no storage: the movement may play again next load */ }
}

/* a failure lands on the settled still, never on half a sentence; the reason is kept on <html> for the probes */
function fail(e) {
  running.forEach(cancel);
  root.dataset.heError = String((e && e.message) || e).slice(0, 160);
  settle();
}

/* ---- let go: the running lights fade where they stand and the hero lands on the settled still in --motion-fast — at once
   from the keyboard. One batch of reads, then the cancels, then the fades, each from where it stood to the settled value ---- */
/* the key never turns back: from the angle where it stands (read from its matrix), forward to 360° — the owner's key */
function landKey(el, transform) {
  if (!el || !transform || transform === 'none') return;
  const m = /matrix3d\(([^)]+)\)/.exec(transform);
  if (!m) return;
  const v = m[1].split(',').map(parseFloat);
  let deg = Math.atan2(-v[2], v[0]) * 180 / Math.PI;   // rotateY(θ): m11 = cos θ, m13 = −sin θ
  if (deg < 0) deg += 360;
  if (!(deg > 1 && deg < 359)) return;
  // forward, never back — at the turn's own pace: an early interruption is a landing, not a 340° whip (motion m-4)
  throughGate(el, [{ transform: `rotateY(${deg}deg)` }, { transform: 'rotateY(360deg)' }],
    { duration: Math.max(T.fast, Math.round((360 - deg) / 360 * 640)), easing: ENTER, fill: 'none' });
}
/* the fades from where they stand: one batch of reads after the pause, then the cancels, then one fade per element */
function fadeWhereTheyStand(list, except) {
  const targets = [...new Set(list.map((a) => a.effect && a.effect.target).filter(Boolean))];
  const snaps = targets.map((el) => { const st = getComputedStyle(el); return { el, opacity: st.opacity, transform: st.transform }; });
  list.forEach(cancel);
  snaps.forEach(({ el, opacity, transform }) => {
    if (except && el === except.el) { except.fn(el, transform); return; }
    const now = getComputedStyle(el);
    if (now.opacity === opacity && now.transform === transform) return;
    throughGate(el, [{ offset: 0, opacity, transform }], { duration: T.fast, easing: ENTER, fill: 'none' });
  });
}
function letGo(immediate = false) {
  if (!discovering) return;
  letGoAt = performance.now();
  const list = running.slice();
  const keyEl = $('.door-stage__key > .kg');
  if (immediate) {   // the keyboard, a hidden tab, a breakpoint: at once (the key alone lands forward)
    const keyAt = keyEl ? getComputedStyle(keyEl).transform : 'none';
    list.forEach(cancel);
    settle();
    landKey(keyEl, keyAt);
    return;
  }
  list.forEach((a) => { try { a.pause(); } catch (e) { /* gone */ } });   // held where they stand: this frame reads nothing
  settle();
  nextFrame().then(() => fadeWhereTheyStand(list, { el: keyEl, fn: landKey }));
}

function armLetGo() {
  const onPress = () => letGo(false);
  const onKey = () => letGo(true);
  const onHide = () => { if (document.visibilityState === 'hidden') letGo(true); };
  const onMode = () => letGo(true);
  hero.addEventListener('pointerdown', onPress, { passive: true });
  hero.addEventListener('keydown', onKey);
  document.addEventListener('visibilitychange', onHide);
  mqDesk.addEventListener('change', onMode);
  mqWide.addEventListener('change', onMode);
  mqLand.addEventListener('change', onMode);
  const io = new IntersectionObserver((entries) => { if (entries.some((e) => e.intersectionRatio < 0.25)) letGo(false); }, { threshold: [0.25] });
  io.observe(hero);
  letGoHandlers = [() => hero.removeEventListener('pointerdown', onPress), () => hero.removeEventListener('keydown', onKey),
    () => document.removeEventListener('visibilitychange', onHide), () => mqDesk.removeEventListener('change', onMode),
    () => mqWide.removeEventListener('change', onMode), () => mqLand.removeEventListener('change', onMode), () => io.disconnect()];
}

function discover() {
  if (discovering) return;
  discovering = true;
  const gen = ++run;
  delete root.dataset.heError;
  endFlow(false);
  hero.classList.remove('is-ajar');                    // the movement starts from REST: the door closed
  let plan;
  // the plan reads the geometry on a clean style — BEFORE the class flip, whose invalidation would otherwise be recalculated
  // inside this task by the first read
  try { plan = buildDiscovery(modeOf()); } catch (e) { hero.classList.add('is-discovering'); fail(e); return; }
  hero.classList.add('is-discovering');
  hero.dataset.heClock = JSON.stringify(plan.plan);
  armLetGo();
  nextFrame().then(() => {
    if (!discovering || gen !== run) return;
    const t0 = document.timeline.currentTime;
    clockEnd = plan.end;
    try { issue(plan, 1, t0); } catch (e) { fail(e); return; }
    nextFrame().then(() => {
      if (!discovering || gen !== run) return;
      try { issue(plan, 2, t0); } catch (e) { fail(e); return; }
      if (!running.length) { settle(); return; }
      Promise.allSettled(running.map((a) => a.finished)).then(() => { if (discovering && gen === run) settle(); });
    });
  });
}

/* the settled still without the movement (a later load of the session, a press before the movement, a failure to start):
   the band and the spill fade in once, 240 ms, after the door has decoded (0 ms under reduced motion) */
function ajar(fade = true) {
  hero.classList.remove('is-priming');
  hero.classList.add('is-ajar');
  if (!fade || stillPage()) return;
  [$('[data-aperture]'), $('[data-spill]'), $('[data-bloom]')].forEach((el) => { if (el) throughGate(el, [{ offset: 0, opacity: 0 }], { duration: 2 * T.fast, easing: ENTER, fill: 'none' }); });
}

/* ---- the trigger: the first LCP entry, the door decoded, the hero (or half the tiles) in view on a visible tab, an idle slot,
   then --motion-wait, then an idle slot for the plan; fallback: load + two frames + 1 s ---- */
function doorDecoded() {
  const img = $('[data-door-img]');
  if (!img) return Promise.resolve();
  if (img.complete) return (img.decode ? img.decode().catch(() => {}) : Promise.resolve());
  return new Promise((r) => { img.addEventListener('load', r, { once: true }); img.addEventListener('error', r, { once: true }); });
}
function whenSeen() {
  const lcp = new Promise((resolve) => {
    let done = false;
    const go = () => { if (!done) { done = true; resolve(); } };
    try {
      const po = new PerformanceObserver((entries) => { if (entries.getEntries().length) { po.disconnect(); go(); } });
      po.observe({ type: 'largest-contentful-paint', buffered: true });
    } catch (e) { /* no LCP API: the fallback below */ }
    const loaded = document.readyState === 'complete' ? Promise.resolve() : new Promise((r) => window.addEventListener('load', r, { once: true }));
    loaded.then(afterPaint).then(() => window.setTimeout(go, 1000));
  });
  const onScreen = new Promise((resolve) => {
    const target = mqDesk.matches ? hero : ($('.he-origins__list') || hero);
    const need = mqDesk.matches ? 0.25 : 0.5;
    const io = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting && e.intersectionRatio >= need) && document.visibilityState === 'visible') { io.disconnect(); resolve(); }
    }, { threshold: [0, need, 1] });
    io.observe(target);
  });
  const idle = () => new Promise((r) => ('requestIdleCallback' in window ? window.requestIdleCallback(r, { timeout: 600 }) : window.setTimeout(r, 1)));
  const beat = () => new Promise((r) => window.setTimeout(r, T.wait));
  const prime = () => { if (!stillPage() && !pressed) hero.classList.add('is-priming'); };   // the score's layers rastered in the wait, not in the first frames
  return Promise.all([lcp, doorDecoded(), onScreen]).then(idle).then(() => { prime(); return beat(); }).then(idle);
}

/* ---- THE REPEATABLE FLOW (V5.5): on the settled hero, the hand sends the light along the one path to the door again, every
   time — the shore's glint, the inlay's light, the gold run, the arch light, the steps' twins at .6 (phones: the spine, the
   junction, the floor run, the steps). Its own short clock (≈ 1.3 s on the desktop, ≈ 1 s on a phone); transform and opacity
   only; cancelled where it stands when the hand leaves. The states the flow lands on (the route lit, the door's answer) are the
   CSS hover / press states, which hold as long as the hand does. ---- */
let flowing = [];
let flowGen = 0;
function buildFlow(mode) {
  const ops = [];
  const later = (batch, fn) => ops.push({ batch, fn });
  const k = kit();
  const { H, stations, litOf, door } = k;
  if (mode === 'desk' || mode === 'compact') {
    const wall = k.clip('.he-wipe--wall'), night = k.clip('.he-wipe--night');
    if (!wall && !night) return null;
    const L = (wall ? wall.w : 0) + (night ? night.w : 0);
    const v = clamp(0.9, L / 700, 1.9);                  // the hand's light: brisker than the discovery's — ≈ 700 ms on any wall from 1280 up
    const tSeam = (wall ? wall.w : 0) / v;
    const T0 = tSeam + ((night ? night.w - 7.5 : 0) + H / 2) / v;
    const A = T0 + 520;                                  // the arch has lit
    const END = A + T.slow + 40;
    clockEnd = END;
    if (mode === 'compact') { const corner = $('[data-corner="maroc"]'); if (drawn(corner)) later(1, () => hold(corner, 'opacity', 0, 60, 240, 320, 1, 0, 'linear', ENTER)); }
    later(1, () => k.wipeH(wall, 0, v, T0 + 200));
    later(1, () => k.wipeH(night, tSeam, v, A));
    later(2, () => k.glint(litOf(0), 0, 160, 420));
    if (wall) [1, 2, 3, 4].forEach((i) => { const st = stations[i]; const node = st && $('.he-station__node', st); if (drawn(node)) later(2, () => k.glint(litOf(i), (k.along(wall.r, node) + H / 2) / v - 40, 120, 360)); });
    k.archLight(later, T0);
    door.treads.forEach((el, j) => { if (el) later(2, () => hold(el, 'opacity', T0 + 110 + j * 70, 140, A - 40, 360, 0.6, 0, ENTER, ENTER)); });
    return { ops, end: END };
  }
  if (mode === 'phone') {
    const spine = k.clip('.he-wipe--spine'), floor = k.clip('.he-wipe--floor');
    const junction = $('[data-junction]');
    if (!spine && !floor) return null;
    const sDur = 220;
    const vS = spine ? (spine.h + H) / sDur : 1;
    const tFloor = sDur + 40, vF = 0.9;
    const T0 = floor ? tFloor + (floor.w + H / 2) / vF : tFloor;
    const A = T0 + 400;
    const END = A + T.slow + 40;
    clockEnd = END;
    later(1, () => k.wipeV(spine, 0, vS, A, true));
    if (drawn(junction)) later(1, () => hold(junction, 'opacity', sDur, T.fast, A, 400, 1, 0, ENTER, ENTER));
    later(1, () => k.wipeH(floor, tFloor, vF, A));
    door.treads.forEach((el, j) => { if (el) later(2, () => hold(el, 'opacity', T0 + j * 70, 140, A, 360, 0.6, 0, ENTER, ENTER)); });
    return { ops, end: END };
  }
  return null;   // landscape phones: the short score has no travelling light; the CSS states alone
}
function endFlow(fade) {
  const list = flowing;
  flowing = [];
  const gen = flowGen;
  if (!list.length) { hero.classList.remove('is-flowing'); return; }
  if (!fade) { list.forEach(cancel); hero.classList.remove('is-flowing'); return; }
  list.forEach((a) => { try { a.pause(); } catch (e) { /* gone */ } });
  nextFrame().then(() => {
    fadeWhereTheyStand(list, null);
    if (gen === flowGen) hero.classList.remove('is-flowing');
  });
}
function flow() {
  if (stillPage() || discovering || !hero.classList.contains('is-ajar')) return;
  endFlow(false);
  const gen = ++flowGen;
  let built;
  try { built = buildFlow(modeOf()); } catch (e) { return; }
  if (!built || !built.ops.length) return;
  hero.classList.add('is-flowing');
  nextFrame().then(() => {
    if (gen !== flowGen) return;
    const t0 = document.timeline.currentTime;
    clockEnd = built.end;
    const made = [];
    try {
      built.ops.forEach((op) => {
        const a = op.fn();
        (Array.isArray(a) ? a : [a]).filter(Boolean).forEach((x) => { try { x.startTime = t0; } catch (e) { /* keeps its own start */ } made.push(x); });
      });
    } catch (e) { made.forEach(cancel); hero.classList.remove('is-flowing'); return; }
    flowing = made;
    if (!made.length) { hero.classList.remove('is-flowing'); return; }
    Promise.allSettled(made.map((a) => a.finished)).then(() => { if (gen === flowGen) { flowing = []; hero.classList.remove('is-flowing'); } });
  });
}

/* ---- the replay: the ajar door closes in 240 ms (its three lights to their closed values, held until the discovery owns them), then
   the discovery plays again from REST — never while it plays, never within 400 ms of an interruption (a press on the replay during
   the movement is that interruption, not a replay), never on a still page ---- */
function closeDoor() {
  const made = [[$('[data-aperture]'), { opacity: 0, transform: 'translateX(100%)' }], [$('[data-spill]'), { opacity: 0 }], [$('[data-bloom]'), { opacity: 0 }]]
    .filter(([el]) => el).map(([el, to]) => throughGate(el, [to], { duration: 2 * T.fast, easing: EXIT, fill: 'forwards' })).filter(Boolean);
  return Promise.allSettled(made.map((a) => a.finished)).then(() => made);
}
function replay() {
  if (stillPage() || discovering || !hero.classList.contains('is-ajar') || performance.now() - letGoAt < 400) return;
  endFlow(false);
  closeDoor().then((fills) => {
    if (!discovering && hero.classList.contains('is-ajar') && !stillPage()) discover();
    fills.forEach(cancel);   // the discovery's own closed values hold from here (is-ajar is off)
  });
}

/* ---- the hand ---- */
let pressed = false;
/* the hand wins over the score on its origin: its scripted colour, stem, lift and eyelet are cancelled and each fades from where it
   stood to the hand's state in --motion-standard — at once from the keyboard (never animate a key) */
const handWins = (key, fade) => {
  const list = scripted.get(key);
  if (!list) return;
  scripted.delete(key);
  const targets = fade ? [...new Set(list.map((a) => a.effect && a.effect.target).filter(Boolean))] : [];
  const snaps = targets.map((el) => { const st = getComputedStyle(el); return { el, opacity: st.opacity, transform: st.transform }; });
  list.forEach(cancel);
  snaps.forEach(({ el, opacity, transform }) => {
    const now = getComputedStyle(el);
    if (now.opacity === opacity && now.transform === transform) return;
    throughGate(el, [{ offset: 0, opacity, transform }], { duration: T.standard, easing: ENTER, fill: 'none' });
  });
};
if (hero) {
  const origins = $$('[data-origin]');
  const PRESS_WAIT = 100;      // ms a finger rests on an origin before its press counts
  const TAP_HOLD = 700;        // ms a tap's state is kept once the finger has lifted
  const finger = (event) => event.pointerType === 'touch' || event.pointerType === 'pen';
  const clearNames = () => $$('.he-plate, .he-origin__word').forEach((el) => { el.style.viewTransitionName = ''; });
  origins.forEach((item) => {
    const link = $('a', item);
    if (!link) return;
    const key = item.dataset.aud;
    link.addEventListener('pointerenter', (event) => {
      handWins(key, true);
      if (event.pointerType === 'mouse' && mqHover.matches) flow();          // the fine pointer's hover: the light runs again
    });
    // the keyboard's share of the repeatable flow (the review fix): focus runs the origin's light along the one path, every time —
    // the states themselves stay instant (CSS, html.he-keys); a blur fades the light where it stands, as a pointer leaving does
    link.addEventListener('focus', () => { handWins(key, false); if (root.classList.contains('he-keys') || link.matches(':focus-visible')) flow(); });
    link.addEventListener('blur', () => { if (flowing.length) endFlow(true); });
    // THE PRESS. A mouse's press is the press: its state at once (WebKit sets :active on touch only with a touch listener; its
    // light ran at the hover). A FINGER'S OR A PEN'S FIRST HAS TO SHOW IT IS NOT THE START OF A SCROLL (the review's M2: the four
    // tiles are the bottom fifth of a phone's first screen, where a thumb starts the scroll, and a flick that began on one flashed
    // its pressed ground, its chip in colour and a bead on the spine): the state and the light are armed PRESS_WAIT after it lands —
    // the browser cancels a scroll's pointer sooner, 53–80 ms as measured — or at once when it lifts before that (a tap). A tap keeps
    // them for TAP_HOLD, while the next page answers (pagehide clears them sooner); a cancelled pointer drops them where they
    // stand. The handler writes after it reads: the light's geometry is read on a clean style, then the class goes on (a11y F3).
    let timer = 0;                                     // the finger's wait, then the tap's release
    let waiting = false;
    let held = false;
    const press = (light) => {
      waiting = false;
      held = true;
      if (light) flow();                               // the finger sends the light, every time (the mouse already has, at the hover)
      link.classList.add('is-pressed');
      clearNames();                                    // view-transition-ready: two names, on the pressed origin alone
      [['.he-plate', 'figure'], ['.he-origin__word', 'word']].forEach(([part, name]) => { const el = $(part, item); if (el) el.style.viewTransitionName = `ile-entrance-${name}`; });
    };
    const release = (fade) => {
      window.clearTimeout(timer);
      waiting = false;
      if (held) link.classList.remove('is-pressed');
      if (held && fade === true && flowing.length) endFlow(true);
      held = false;
    };
    link.addEventListener('pointerdown', (event) => {
      pressed = true;
      release();
      if (!finger(event)) { press(event.pointerType !== 'mouse'); return; }
      waiting = true;
      timer = window.setTimeout(press, PRESS_WAIT, true);
    }, { passive: true });
    link.addEventListener('pointerup', (event) => {
      if (!finger(event)) { release(); return; }
      if (waiting) { window.clearTimeout(timer); press(true); }   // a tap shorter than the wait: its state and its light now
      timer = window.setTimeout(release, TAP_HOLD);
    }, { passive: true });
    link.addEventListener('pointercancel', () => { if (held) clearNames(); release(true); }, { passive: true });   // a scroll, a long press's menu: no press — the light fades where it stands
    link.addEventListener('pointerleave', (event) => {
      if (finger(event)) return;                       // a finger that lifts leaves too: its tap is released by its own clock
      release();
      if (flowing.length) endFlow(true);
    }, { passive: true });
  });
  const clearPress = () => $$('.he-origin__link.is-pressed').forEach((el) => el.classList.remove('is-pressed'));
  window.addEventListener('pagehide', () => { clearNames(); clearPress(); endFlow(false); });
  window.addEventListener('pageshow', (e) => { if (e.persisted) { clearNames(); clearPress(); } });

  // THE REPLAY — the button over the golden key (templates/pages/home/_hero.html, .he-replay): Enter, Space or a click plays the
  // whole sequence again from the closed door; drawn only here, on a page that moves (never under reduced motion or forced colours)
  const replayButton = $('[data-replay]');
  if (replayButton && !stillPage()) {
    hero.classList.add('has-replay');
    replayButton.addEventListener('click', replay);
  }

  // THE LIGHT AGAIN, WHERE NOTHING HOVERS (the review's M4). On a touch screen the movement could be seen again only through the
  // button over the key, and a tap's light is cut by the page it opens. So each time the hero comes back into view after having
  // left it — the niche out of sight, then most of it in sight again — the hand's short light runs once along the one path to the
  // door (the flow above: ≈ 1 s, the key does not turn). Never under reduced motion or forced colours, never during the discovery
  // (flow() asks); the whole sequence stays on the key.
  const niche = $('[data-niche]');
  if (niche && 'IntersectionObserver' in window) {
    let away = false;
    new IntersectionObserver((entries) => {
      const seen = entries[entries.length - 1];
      if (!seen.isIntersecting) { away = true; return; }
      if (!away || seen.intersectionRatio < 0.6 || !mqTouch.matches) return;
      away = false;
      flow();
    }, { threshold: [0, 0.6] }).observe(niche);
  }

  // ---- start ------------------------------------------------------------------------------------------
  const seen = (() => { try { return window.sessionStorage.getItem(SEEN_KEY) === '1'; } catch (e) { return false; } })();
  if (stillPage()) {
    ajar(false);
  } else if (seen) {
    doorDecoded().then(() => ajar(true));
  } else {
    hero.addEventListener('pointerdown', () => { pressed = true; }, { once: true, passive: true });
    whenSeen().then(() => {
      if (stillPage()) { ajar(false); return; }
      if (pressed) { ajar(true); return; }
      discover();
    });
  }
}
