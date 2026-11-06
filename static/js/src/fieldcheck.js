/**
 * THE INLINE CHECK of the form system (V5.12 W2, lane B; DECISIONS §5.5, §5.8, §5.9, M10) — loaded by the form
 * pages only: the field partial brings it once per response ({% form_assets %}, apps/core/templatetags/ile_forms.py).
 *
 * The server stays the judge: its summary and each field's error are untouched, nothing is ever blocked — not the
 * typing, not the submission. This module only says EARLIER what the server would say, in the server's own words (the
 * field's `data-msg-*`: required, type, max / min length, low / high), read off the native constraint validation:
 *   - on blur, a touched field is checked; then on input, so a correction clears its error as it is typed (an
 *     untouched box or choice is not checked on blur: only once changed, or at «Continuer» and the submission);
 *   - an error writes the message row (one polite live region per field), `aria-invalid` and the `_error` id the
 *     control names; the edge and the status mark follow (core/forms.css), never colour alone;
 *   - a WARNING never blocks: Caps Lock on a password, a textarea a tenth from its limit;
 *   - a SUCCESS only for a confirmed value: the second password equal to the first (DECISIONS §5.4) — its words and
 *     its edge; no script draws a check (O14: tests/frontend/test_o14_lint.py).
 * It also enhances, progressively: the date into day / month / year segments (the native input kept as the hidden ISO
 * value the form submits), the number with its − / + stepper, and — through combobox.js, fetched only where a select
 * has more than fifteen options — the long selects. Event delegation on the document: a fragment swapped in by htmx
 * is checked as it is; `htmx:load` enhances its dates, numbers and selects.
 * A FRAGMENT FETCHED BY SCRIPT (the preview drawer's DOMParser + replaceChildren) does not run the module script
 * {% form_assets %} put in it — a script parsed that way is inert. Its fields still submit and the server still
 * judges; to check them inline, the host module imports this one and dispatches `fields:load` on the inserted root
 * (`root.dispatchEvent(new CustomEvent("fields:load", { bubbles: true }))`), as htmx's `htmx:load` does.
 * V5.15 W3 (lane B): the new password's live checklist (`[data-pw-rules]`, DECISIONS §5.11) and, for a multi-step
 * form, steps.js — fetched where a `form[data-steps]` is — which asks `validate(step)` before it moves on.
 * CSP: no inline style, no string evaluated; every word is the page's.
 */

const FIELD = "[data-field]";
const CONTROL = "input:not([type=hidden]):not([data-combobox-native]), select:not([data-combobox-native]), textarea";
const NS = "http://www.w3.org/2000/svg";
const touched = new WeakSet();
const isChoice = (control) => control?.type === "checkbox" || control?.type === "radio";
/** A control whose field came back from the server with an error, and the value it came back with: that error is
 *  the server's (an address already used, a code that expired…) and stands until the value changes. */
const served = new WeakMap();
let sprite;

/** The chrome sprite's URL, read off a mark the page already draws (its content hash, or the manifest's name). */
function glyph(name, cls = "icon") {
  if (sprite === undefined) {
    sprite = "";
    for (const use of document.querySelectorAll("use")) {
      const href = use.getAttribute("href") || "";
      if (/\/icons(\.[0-9a-f]{8,})?\.svg/.test(href)) { sprite = href.split("#")[0]; break; }
    }
  }
  if (!sprite) return null;
  const svg = document.createElementNS(NS, "svg");
  svg.setAttribute("class", cls);
  svg.setAttribute("aria-hidden", "true");
  svg.setAttribute("focusable", "false");
  const use = document.createElementNS(NS, "use");
  use.setAttribute("href", `${sprite}#icon-${name}`);
  svg.append(use);
  return svg;
}

const msgOf = (wrap, key, n) => (wrap.dataset[`msg${key[0].toUpperCase()}${key.slice(1)}`] || "").replace(/\{n\}|%\(n\)s/g, n ?? "");

/** What the server would say of this control now, or "". */
function problem(wrap, control) {
  const v = control.validity;
  if (!v || v.valid) return "";
  if (v.valueMissing) return msgOf(wrap, "required");
  if (v.tooLong) return msgOf(wrap, "max", control.value.length);
  if (v.tooShort) return msgOf(wrap, "min", control.value.length);
  if (v.rangeUnderflow) return msgOf(wrap, "low");
  if (v.rangeOverflow) return msgOf(wrap, "high");
  return msgOf(wrap, "type");
}

function describe(control, id, on) {
  const ids = new Set((control.getAttribute("aria-describedby") || "").split(/\s+/).filter(Boolean));
  if (on) ids.add(id); else ids.delete(id);
  if (ids.size) control.setAttribute("aria-describedby", [...ids].join(" "));
  else control.removeAttribute("aria-describedby");
}

/** One state per field: "" · error · warning · success — the message row, the status mark, the classes. */
function setState(wrap, control, kind, text, lang = "") {
  const row = wrap.querySelector(":scope > .form-field__msg > .form-field__msg-in");
  const status = wrap.querySelector(".form-field__status");
  const id = `${control.id}_error`;
  wrap.classList.toggle("form-field--error", kind === "error");
  wrap.classList.toggle("form-field--warning", kind === "warning");
  wrap.classList.toggle("form-field--success", kind === "success");
  if (kind === "error") control.setAttribute("aria-invalid", "true");
  else control.removeAttribute("aria-invalid");
  if (row) {
    const current = row.firstElementChild;
    if (!kind) {
      if (current) current.remove();
    } else if (!current || current.dataset.kind !== kind || current.textContent !== text) {
      let box;
      if (kind === "error") {
        box = document.createElement("div");
        box.className = "form-field__errors";
        box.id = id;
        const ul = document.createElement("ul");
        ul.className = "form-field__error-list";
        const li = document.createElement("li");
        li.textContent = text;
        if (lang) li.lang = lang;
        ul.append(li);
        box.append(ul);
      } else {
        box = document.createElement("p");
        box.className = `form-field__note form-field__note--${kind}`;
        box.id = id;
        // a warning carries its mark; a confirmation is said by its words and its edge — no script draws a check (O14)
        const mark = kind === "warning" ? glyph("warning") : null;
        if (mark) box.append(mark);
        const words = document.createElement("span");
        words.textContent = text;
        if (lang) words.lang = lang;
        box.append(words);
      }
      box.dataset.kind = kind;
      row.replaceChildren(box);
    }
  }
  describe(control, id, Boolean(kind));
  if (status && !wrap.classList.contains("form-field--readonly")) {
    const mark = { error: "circle-alert", warning: "warning" }[kind];
    status.replaceChildren(...(mark && glyph(mark) ? [glyph(mark)] : []));
  }
}

/** The two passwords: equal → the confirmed value's check; different, once the second is left → the error. */
function matchState(wrap, control, leaving) {
  const first = document.getElementById(wrap.dataset.match);
  if (!first || !control.value) return null;
  if (control.value === first.value) return ["success", msgOf(wrap, "matched")];
  return leaving ? ["error", msgOf(wrap, "match")] : null;
}

function check(wrap, control, leaving = false) {
  if (served.has(control) && served.get(control) === control.value) return;
  served.delete(control);
  if (wrap.matches("[data-date]")) return checkDate(wrap, leaving);
  const text = problem(wrap, control);
  if (text) return setState(wrap, control, "error", text);
  if (wrap.dataset.match) {
    const state = matchState(wrap, control, leaving);
    return state ? setState(wrap, control, ...state) : setState(wrap, control, "", "");
  }
  const counter = wrap.querySelector("[data-count-of]");
  if (counter) {
    const left = Number(counter.dataset.max) - control.value.length;
    if (left <= Number(counter.dataset.max) / 10) return setState(wrap, control, "warning", msgOf(wrap, "near", left), wrap.dataset.msgNearLang || "");
  }
  if (wrap.dataset.caps === "on") return setState(wrap, control, "warning", msgOf(wrap, "caps"));
  return setState(wrap, control, "", "");
}

function count(wrap, control) {
  const counter = wrap.querySelector("[data-count-of] [data-count]");
  if (counter) counter.textContent = String(control.value.length);
}

function context(target) {
  const wrap = target.closest?.(FIELD);
  if (!wrap || wrap.matches("[data-choices]")) return [null, null];
  const control = wrap.matches("[data-date]") ? wrap.querySelector("[data-date-segments] input") : wrap.querySelector(CONTROL);
  return [wrap, control];
}

// ---- the date in three segments ------------------------------------------------------------------------------
const SEGMENTS = [["day", 2], ["month", 2], ["year", 4]];

function dateValue(wrap) {
  const [d, m, y] = [...wrap.querySelectorAll("[data-date-segments] input")].map((i) => i.value.trim());
  if (!d && !m && !y) return { iso: "", empty: true, valid: true };
  const iso = `${y.padStart(4, "0")}-${m.padStart(2, "0")}-${d.padStart(2, "0")}`;
  const date = new Date(`${iso}T00:00:00Z`);
  const valid = y.length === 4 && date.getUTCFullYear() === Number(y) && date.getUTCMonth() + 1 === Number(m) && date.getUTCDate() === Number(d);
  return { iso: valid ? iso : `${y}-${m}-${d}`, empty: false, valid };
}

function checkDate(wrap, leaving) {
  const native = wrap.querySelector("[data-date-native]");
  const first = wrap.querySelector("[data-date-segments] input");
  const value = dateValue(wrap);
  native.value = value.iso;
  const required = native.hasAttribute("data-required");
  let text = "";
  if (value.empty && required && leaving) text = msgOf(wrap, "required");
  else if (!value.empty && !value.valid && leaving) text = msgOf(wrap, "type");
  for (const input of wrap.querySelectorAll("[data-date-segments] input")) {
    if (text) input.setAttribute("aria-invalid", "true"); else input.removeAttribute("aria-invalid");
  }
  setState(wrap, first, text ? "error" : "", text);
}

function enhanceDate(wrap) {
  const native = wrap.querySelector("input[type=date], input:not([type=hidden])");
  if (!native || wrap.querySelector("[data-date-segments]")) return;
  const label = wrap.querySelector(".form-field__label");
  const labelId = `${native.id}_label`;
  if (label) label.id = labelId;
  const group = document.createElement("div");
  group.className = "date-field__segments";
  group.setAttribute("role", "group");
  if (label) group.setAttribute("aria-labelledby", labelId);
  group.dataset.dateSegments = "";
  const [y, m, d] = (native.value || "").split("-");
  const values = { day: d || "", month: m || "", year: y || "" };
  const purpose = native.getAttribute("autocomplete") === "bday";
  for (const [key, size] of SEGMENTS) {
    const seat = document.createElement("div");
    seat.className = `date-field__segment date-field__segment--${key}`;
    const input = document.createElement("input");
    input.type = "text";
    input.id = key === "day" ? native.id : `${native.id}_${key}`;
    input.inputMode = "numeric";
    input.maxLength = size;
    input.dir = "ltr";
    input.value = values[key];
    input.autocomplete = purpose ? `bday-${key}` : "off";
    if (native.required) input.setAttribute("aria-required", "true");
    const described = native.getAttribute("aria-describedby");
    if (described) input.setAttribute("aria-describedby", described);
    const small = document.createElement("label");
    small.htmlFor = input.id;
    small.textContent = wrap.dataset[`label${key[0].toUpperCase()}${key.slice(1)}`] || key;
    seat.append(small, input);
    group.append(seat);
  }
  native.id = `${native.id}_iso`;
  if (native.required) native.setAttribute("data-required", "");
  native.required = false;
  native.type = "hidden";
  native.dataset.dateNative = "";
  native.after(group);
  if (label) label.htmlFor = group.querySelector("input").id;
}

function onDateInput(event) {
  const input = event.target;
  const wrap = input.closest("[data-date]");
  input.value = input.value.replace(/\D+/g, "");
  if (event.inputType?.startsWith("insert") && input.value.length >= input.maxLength) {
    const seats = [...wrap.querySelectorAll("[data-date-segments] input")];
    seats[seats.indexOf(input) + 1]?.focus();
  }
  checkDate(wrap, false);
}

// ---- the number stepper ----------------------------------------------------------------------------------------
function bounds(input, buttons) {
  const value = input.valueAsNumber;
  for (const button of buttons) {
    const down = button.dataset.step === "-1";
    const limit = down ? input.min : input.max;
    button.disabled = limit !== "" && !Number.isNaN(value) && (down ? value <= Number(limit) : value >= Number(limit));
  }
}

function enhanceNumber(wrap) {
  const input = wrap.querySelector("input");
  const buttons = wrap.querySelectorAll("[data-step]");
  if (!input || !buttons.length || wrap.dataset.numberReady) return;
  wrap.dataset.numberReady = "1";
  if (!input.inputMode) input.inputMode = "numeric";
  for (const button of buttons) {
    button.hidden = false;
    button.addEventListener("click", () => {
      if (button.dataset.step === "-1") input.stepDown(); else input.stepUp();
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.dispatchEvent(new Event("change", { bubbles: true }));
    });
  }
  input.addEventListener("input", () => bounds(input, buttons));
  bounds(input, buttons);
}

// ---- a step of a multi-step form (V5.15 W3; static/js/src/steps.js asks before it moves on) ---------------------
/** Check every field of `scope` as if it had been left — the server's words, the same rows — and return the first
 *  control in error, or null. A required group of cards with nothing chosen says the server's «required».
 *  `quiet`: only ask — nothing is painted (steps.js, to know where a reloaded or deep-linked form may open). */
function validate(scope, quiet = false) {
  let first = null;
  for (const wrap of scope.querySelectorAll(FIELD)) {
    if (wrap.matches("[data-choices]")) {
      const inputs = [...wrap.querySelectorAll("input")];
      if (inputs.some((input) => input.required) && !inputs.some((input) => input.checked)) {
        if (!quiet) {
          wrap.classList.add("choices--error");
          setState(wrap, inputs[0], "error", msgOf(wrap, "required"));
        }
        first ??= inputs[0];
      }
      continue;
    }
    const [field, control] = context(wrap);
    if (!field || !control) continue;
    if (quiet) {
      const date = field.matches("[data-date]") && dateValue(field);
      const bad = date ? (date.empty ? field.querySelector("[data-date-native]")?.hasAttribute("data-required") : !date.valid) : problem(field, control);
      if (bad) first ??= control;
      continue;
    }
    touched.add(field);
    check(field, control, true);
    if (field.classList.contains("form-field--error")) first ??= control;
  }
  return first;
}

// ---- the new password's checklist (V5.15 W3; DECISIONS §5.11) -------------------------------------------------
const said = new WeakMap();
/** Each rule the browser can verify, marked as it is typed (a plain disc, never a tick: O14); the count said once,
 *  politely, when the typing pauses. A rule only the server judges stays neutral. */
function rules(control) {
  const list = document.querySelector(`[data-pw-rules="${control.id}"]`);
  if (!list) return;
  const value = control.value;
  let met = 0;
  let total = 0;
  for (const item of list.children) {
    const rule = item.dataset.rule || "";
    let ok = null;
    if (rule.startsWith("min:")) ok = value.length >= Number(rule.slice(4));
    else if (rule === "notnumeric") ok = value.length > 0 && !/^\d+$/.test(value);
    if (ok === null) continue;
    total += 1;
    if (ok) met += 1;
    item.dataset.met = ok ? "1" : "";
    const state = item.querySelector(".pw-rule__state");
    if (state) state.textContent = ok ? state.dataset.stateMet : state.dataset.stateUnmet;
  }
  const summary = list.parentElement.querySelector("[data-pw-summary]");
  if (!summary) return;
  clearTimeout(said.get(summary));
  said.set(summary, setTimeout(() => {
    summary.textContent = (summary.dataset.msg || "").replace("%(n)s", String(met)).replace("%(total)s", String(total));
    if (summary.dataset.msgLang) summary.lang = summary.dataset.msgLang;
  }, 900));
}

// ---- wiring ----------------------------------------------------------------------------------------------------
function enhance(root = document) {
  for (const box of root.querySelectorAll(".form-field__msg-in > .form-field__errors:not([data-kind])")) {
    const [, control] = context(box);
    if (control) served.set(control, control.value);
  }
  for (const wrap of root.querySelectorAll("[data-date]")) enhanceDate(wrap);
  for (const wrap of root.querySelectorAll("[data-number]")) enhanceNumber(wrap);
  if (root.querySelector("[data-combobox]")) import("./combobox.js").then((m) => m.initComboboxes(root));
  if (root.querySelector("form[data-steps]")) import("./steps.js").then((m) => m.initSteps(root, { validate, glyph }));
}

document.addEventListener("focusout", (event) => {
  const [wrap, control] = context(event.target);
  if (!wrap) return;
  if (wrap.matches("[data-date]") && wrap.contains(event.relatedTarget)) return;
  // (F1) a box or a choice nobody has touched has no half-typed value to check: tabbing past it says nothing; it is
  // checked once changed (below, on input) and at «Continuer» / the submission (validate)
  if (isChoice(control) && !touched.has(wrap) && !wrap.classList.contains("form-field--error")) return;
  touched.add(wrap);
  check(wrap, control, true);
});

document.addEventListener("input", (event) => {
  if (event.target.closest?.("[data-date-segments]")) return onDateInput(event);
  const [wrap, control] = context(event.target);
  if (!wrap) return;
  count(wrap, control);
  if (control.type === "password") rules(control);
  if (isChoice(control)) touched.add(wrap);
  if (touched.has(wrap) || wrap.classList.contains("form-field--error") || wrap.dataset.match) check(wrap, control);
  // the first password changed: its twin is checked again
  const twin = document.querySelector(`${FIELD}[data-match="${control.id}"]`);
  if (twin && touched.has(twin)) check(twin, twin.querySelector(CONTROL));
});

document.addEventListener("change", (event) => {
  // the file zone says the chosen file (its name, in its own order)
  const zone = event.target.closest?.("[data-filezone]");
  if (zone && event.target.files) {
    const name = zone.querySelector("[data-file-name]");
    if (name) name.textContent = [...event.target.files].map((file) => file.name).join(", ");
    zone.classList.toggle("has-file", event.target.files.length > 0);
  }
  const group = event.target.closest?.("[data-choices]");
  if (group && group.classList.contains("form-field--error") && group.querySelector("input:checked")) {
    group.classList.remove("form-field--error", "choices--error");
    group.querySelector(".form-field__msg-in")?.replaceChildren();
    for (const input of group.querySelectorAll("input")) input.removeAttribute("aria-invalid");
  }
});

function caps(event) {
  if (event.target.type !== "password" || typeof event.getModifierState !== "function") return;
  const [wrap, control] = context(event.target);
  if (!wrap || !wrap.dataset.msgCaps) return;
  const on = event.getModifierState("CapsLock") ? "on" : "";
  if ((wrap.dataset.caps || "") === on) return;
  wrap.dataset.caps = on;
  if (!wrap.classList.contains("form-field--error")) check(wrap, control);
}
document.addEventListener("keydown", caps);
document.addEventListener("keyup", caps);

document.addEventListener("htmx:load", (event) => enhance(event.target));
document.addEventListener("fields:load", (event) => enhance(event.target));
enhance();
