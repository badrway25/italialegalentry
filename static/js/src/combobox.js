/**
 * THE COMBOBOX — a long select made searchable (V5.12 W2, lane B; DECISIONS §5.7; 21st.dev «Combobox» 34726, its
 * behaviour only: no React, no Tailwind). Fetched by fieldcheck.js only where a field says `data-combobox` (a select
 * of more than fifteen options: the country, the nationality…); everywhere else the select stays native.
 *
 * Progressive: the native <select> keeps its name and is what the form submits; it is hidden only once this module
 * has built its text input, which takes the select's id (so the label still names it), its `required`, its
 * description and its value's label. The pattern is the ARIA 1.2 «combobox with listbox popup»: `role="combobox"`,
 * `aria-expanded`, `aria-controls`, `aria-activedescendant`; ArrowDown / ArrowUp move, Enter chooses, Escape closes
 * and restores, Alt+ArrowDown opens; a pointer chooses on press. The filter ignores case and diacritics («cote» finds
 * «Côte d’Ivoire»), names that START with the text first. Leaving with a text that names no option restores the chosen
 * one; leaving it empty clears the choice. The count of matches is said once, politely, in the field's own words
 * (`data-msg-count`, `data-msg-none`). No inline style (CSP); the list's look is core/forms.css.
 */

const fold = (text) => text.normalize("NFD").replace(/\p{M}+/gu, "").replace(/[’']/g, "'").toLocaleLowerCase().trim();
let serial = 0;

function build(seat) {
  const select = seat.querySelector("select");
  if (!select || seat.dataset.comboReady) return;
  seat.dataset.comboReady = "1";
  seat.classList.add("combo");
  const options = [...select.options].filter((o) => o.value !== "").map((o) => ({ value: o.value, label: o.text, key: fold(o.text) }));
  const id = select.id;
  const listId = `${id}-list`;
  const input = document.createElement("input");
  input.type = "text";
  input.className = "combo__input";
  input.id = id;
  input.setAttribute("role", "combobox");
  input.setAttribute("aria-autocomplete", "list");
  input.setAttribute("aria-expanded", "false");
  input.setAttribute("aria-controls", listId);
  input.autocomplete = "off";
  input.spellcheck = false;
  input.required = select.required;
  for (const name of ["aria-describedby", "aria-invalid"]) if (select.hasAttribute(name)) input.setAttribute(name, select.getAttribute(name));
  input.value = select.value ? select.selectedOptions[0].text : "";
  const list = document.createElement("ul");
  list.className = "combo__list";
  list.id = listId;
  list.setAttribute("role", "listbox");
  list.hidden = true;
  const label = document.querySelector(`label[for="${CSS.escape(id)}"]`);
  if (label) { label.id ||= `${id}-label`; list.setAttribute("aria-labelledby", label.id); }
  const status = document.createElement("span");
  status.className = "visually-hidden";
  status.setAttribute("role", "status");
  select.id = `${id}-native`;
  select.dataset.comboboxNative = "";
  select.tabIndex = -1;
  select.setAttribute("aria-hidden", "true");
  select.before(input);
  input.after(list, status);

  const prefix = `combo${(serial += 1)}-`;
  let shown = [];
  let active = -1;

  const render = () => {
    const text = fold(input.value);
    const starts = [];
    const contains = [];
    for (const option of options) {
      if (!text || option.key.startsWith(text)) starts.push(option);
      else if (option.key.includes(text)) contains.push(option);
    }
    shown = [...starts, ...contains];
    list.replaceChildren(...shown.map((option, index) => {
      const li = document.createElement("li");
      li.className = "combo__option";
      li.id = `${prefix}${index}`;
      li.setAttribute("role", "option");
      li.setAttribute("aria-selected", String(option.value === select.value));
      li.textContent = option.label;
      li.addEventListener("pointerdown", (event) => { event.preventDefault(); choose(option); });
      return li;
    }));
    if (!shown.length) {
      const li = document.createElement("li");
      li.className = "combo__empty";
      li.setAttribute("role", "presentation");
      li.textContent = seat.dataset.msgNone || "";
      list.append(li);
    }
    status.textContent = shown.length ? (seat.dataset.msgCount || "").replace("%(n)s", shown.length) : seat.dataset.msgNone || "";
    if (shown.length && seat.dataset.msgCountLang) status.lang = seat.dataset.msgCountLang; else status.removeAttribute("lang");
    move(shown.length ? 0 : -1);
  };
  const move = (index) => {
    list.querySelector(".is-active")?.classList.remove("is-active");
    active = index;
    if (index < 0) { input.removeAttribute("aria-activedescendant"); return; }
    const li = list.children[index];
    li.classList.add("is-active");
    input.setAttribute("aria-activedescendant", li.id);
    li.scrollIntoView({ block: "nearest" });
  };
  const open = () => { if (list.hidden) { list.hidden = false; input.setAttribute("aria-expanded", "true"); render(); } };
  const close = () => { list.hidden = true; input.setAttribute("aria-expanded", "false"); input.removeAttribute("aria-activedescendant"); };
  const choose = (option) => {
    select.value = option ? option.value : "";
    input.value = option ? option.label : "";
    select.dispatchEvent(new Event("change", { bubbles: true }));
    input.dispatchEvent(new Event("input", { bubbles: true }));
    close();
  };

  input.addEventListener("input", (event) => { if (event.isTrusted) { open(); render(); } });
  input.addEventListener("click", open);
  input.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      if (list.hidden || event.altKey) open(); else if (shown.length) move(Math.min(active + 1, shown.length - 1));
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      if (!list.hidden && shown.length) move(Math.max(active - 1, 0));
    } else if (event.key === "Enter" && !list.hidden) {
      event.preventDefault();
      if (active >= 0) choose(shown[active]);
    } else if (event.key === "Escape" && !list.hidden) {
      event.preventDefault();
      input.value = select.value ? select.selectedOptions[0].text : "";
      close();
    }
  });
  input.addEventListener("blur", () => {
    const text = fold(input.value);
    if (!text) { if (select.value) choose(null); else close(); return; }
    const exact = options.find((option) => option.key === text);
    if (exact) choose(exact);
    else { input.value = select.value ? select.selectedOptions[0].text : ""; close(); }
  });
}

export function initComboboxes(root = document) {
  for (const seat of root.querySelectorAll("[data-combobox]")) build(seat);
}
