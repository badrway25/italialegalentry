/**
 * THE REVIEW OF A MULTI-STEP FORM (V5.15 W3, lane B; DECISIONS §5.12) — fetched by steps.js when the last step of a
 * `[data-steps-review-on]` form is first reached (the company's need, the «Recueil des besoins»): what was typed,
 * step by step, each with «Modifier» — written with textContent from the fields themselves, never a password.
 * Round 1: a REQUIRED field still empty is not a quiet «not given» — it is an error row in the server's own words
 * (the field's `data-msg-required`) with its way back to the field; an optional one left empty is a dash.
 */

const el = (tag, cls, text) => {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text !== undefined) node.textContent = text;
  return node;
};

/** The words of a field: its label without «facultatif» / «obligatoire» and without hidden helpers. */
function labelOf(wrap) {
  const node = wrap.querySelector(":scope > .form-field__label, :scope > .choices__legend, :scope .form-field__check > label");
  if (!node) return "";
  const copy = node.cloneNode(true);
  for (const extra of copy.querySelectorAll(".form-field__optional, .visually-hidden")) extra.remove();
  return copy.textContent.replace(/\s+/g, " ").trim();
}

/** What the person gave: the chosen cards, the option, the date, the text — "" when nothing; null for a password. */
function valueOf(wrap, yes, no) {
  if (wrap.matches("[data-choices]")) {
    return [...wrap.querySelectorAll("input:checked")]
      .map((input) => input.closest(".choice")?.querySelector(".choice__title")?.textContent.trim() || "")
      .filter(Boolean)
      .join(", ");
  }
  if (wrap.querySelector("input[type=password]")) return null;
  const box = wrap.querySelector("input[type=checkbox]");
  if (box) return box.checked ? yes : no;
  const select = wrap.querySelector("select");
  if (select) return select.value ? select.selectedOptions[0]?.textContent.trim() || "" : "";
  const parts = [...wrap.querySelectorAll("[data-date-segments] input")].map((input) => input.value.trim());
  if (parts.length) return parts.some(Boolean) ? parts.join(".") : "";
  const control = wrap.querySelector("textarea, input:not([type=hidden])");
  return control ? control.value.trim() : "";
}

const isRequired = (wrap) => wrap.classList.contains("form-field--required") || Boolean(wrap.querySelector("[required], [aria-required='true'], [data-required]"));

/** Write the review into `seat`: `steps` (the fieldsets before the last), their `labels`, and from steps.js `msg`,
 *  `word` (a node in the word's language), `glyph` and `goTo(i, options)`. */
export function drawReview(seat, steps, labels, { msg, word, glyph, goTo }) {
  const parts = steps.map((step, k) => {
    const part = el("section", "form-review__part");
    const top = el("div", "form-review__head");
    const title = el("h3", "form-review__title", labels[k]);
    if (step.dataset.stepLang) title.lang = step.dataset.stepLang;
    const edit = el("button", "form-review__edit");
    edit.type = "button";
    edit.append(glyph("pencil"), word("span", "", "edit"));
    edit.setAttribute("aria-label", `${msg("edit")} — ${labels[k]}`);
    edit.addEventListener("click", () => goTo(k, { check: false }));
    top.append(title, edit);
    const dl = el("dl", "form-review__list");
    for (const wrap of step.querySelectorAll("[data-field]")) {
      const value = valueOf(wrap, msg("yes"), msg("no"));
      if (value === null) continue;
      const dd = el("dd");
      if (value) {
        dd.textContent = value;
      } else if (isRequired(wrap) && wrap.dataset.msgRequired) {
        // the missing answer: the server's words and the way to the field
        dd.className = "is-missing";
        const fix = el("button", "form-review__fix");
        fix.type = "button";
        fix.append(glyph("circle-alert"), el("span", "", wrap.dataset.msgRequired));
        fix.addEventListener("click", () => {
          goTo(k, { check: false, focus: false });
          wrap.querySelector("input:not([type=hidden]), select, textarea")?.focus();
        });
        dd.append(fix);
      } else {
        dd.className = "is-empty";
        dd.textContent = "—";
      }
      dl.append(el("dt", "", labelOf(wrap)), dd);
    }
    part.append(top, dl);
    part.classList.toggle("has-missing", Boolean(dl.querySelector(".is-missing")));
    return part;
  });
  seat.replaceChildren(...parts);
  seat.hidden = false;
}
