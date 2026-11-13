/**
 * «La ricerca» — the reading pages' live search (FINAL MICRO-PASS, 9 Nov 2026; BRIEF §6 B1 the FAQ, B2 the glossary),
 * after 21st.dev «Searchable Question Index» (ibrandify/searchable-question-index, id 37558): the list answers as one
 * types, a pill narrows it to a theme, a live count says how many entries answer, and an empty state offers the way
 * back. Adapted, not copied (a React component there; native APIs here, on the server's markup): no word is written by
 * this module — every sentence is the page's own (the count's for 0 … n in a <template>, rendered in the page's
 * language and plural forms).
 *
 * Markup (templates/faq/index.html, templates/glossary/index.html):
 *   [data-cerca="<field id>"]  the list's root; the field is document.getElementById(<field id>), and its form stops
 *                              going to the server while the list answers live (the server's ?q= stays the no-script
 *                              path, and the results page's own);
 *   [data-cerca-voce]          an entry: the words of its [data-cerca-testo] parts (the question and the answer, the
 *                              term and the definition) — accents and case folded — are what a query matches;
 *                              `data-tema` its theme;
 *   [data-cerca-tema]          a pill (aria-pressed): its theme, "" for all;
 *   [data-cerca-conto]         the live count (role=status), spoken while a query or a theme narrows the list; its
 *                              sentences the children of <template data-cerca-conti>, the n-th saying n;
 *   [data-cerca-vuoto]         the empty state; [data-cerca-azzera] in it gives every entry back.
 * The root carries data-cerca-attiva while the list is narrowed. A link of the root that is not an entry's (the
 * glossary's letters) gives every entry back before it is followed, so it always lands. The address's entry (#key), a
 * <details> row, opens on arrival and on hashchange — given back first if a filter hid it, then placed under the
 * letterhead (no FAQ row waits for the rise: cms/_faq-v2.css).
 */
const fold = (text) => text.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();

for (const root of document.querySelectorAll("[data-cerca]")) {
  const field = document.getElementById(root.dataset.cerca);
  if (!field) continue;
  const form = field.form;
  const clear = form && form.querySelector(".cerca__pulisci");
  const items = [...root.querySelectorAll("[data-cerca-voce]")];
  const words = items.map((item) =>
    fold([...item.querySelectorAll("[data-cerca-testo]")].map((part) => part.textContent).join(" ") || item.textContent),
  );
  const pills = [...root.querySelectorAll("[data-cerca-tema]")];
  const count = root.querySelector("[data-cerca-conto]");
  const said = root.querySelector("template[data-cerca-conti]");
  const sentences = said ? [...said.content.children].map((sentence) => sentence.textContent) : [];
  const empty = root.querySelector("[data-cerca-vuoto]");
  let theme = "";

  const apply = () => {
    const query = fold(field.value.trim());
    let shown = 0;
    items.forEach((item, k) => {
      const on = (!theme || item.dataset.tema === theme) && (!query || words[k].includes(query));
      item.hidden = !on;
      shown += on;
    });
    const narrowed = Boolean(query || theme);
    root.toggleAttribute("data-cerca-attiva", narrowed);
    if (count) count.textContent = narrowed ? sentences[shown] || "" : "";
    if (empty) empty.hidden = shown > 0;
    if (clear) clear.hidden = !field.value;
    pills.forEach((pill) => pill.setAttribute("aria-pressed", String(pill.dataset.cercaTema === theme)));
  };

  const reset = () => {
    field.value = "";
    theme = "";
    apply();
  };

  const arrive = (event) => {
    const target = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!target || !items.includes(target)) return;
    if (target.tagName === "DETAILS") target.open = true;
    if (target.hidden) {
      reset();
      // a row a filter hid had no box when the address changed: given back, it is placed where the browser would have
      if (event) target.scrollIntoView();
    }
  };

  field.addEventListener("input", apply);
  field.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && field.value) {
      event.preventDefault();
      reset();
    }
  });
  if (form) form.addEventListener("submit", (event) => event.preventDefault());
  if (clear) {
    clear.addEventListener("click", () => {
      reset();
      field.focus();
    });
  }
  pills.forEach((pill) =>
    pill.addEventListener("click", () => {
      theme = pill.dataset.cercaTema;
      apply();
    }),
  );
  root.addEventListener("click", (event) => {
    const link = event.target.closest("a[href^='#']");
    if (link && !link.closest("[data-cerca-voce]") && root.hasAttribute("data-cerca-attiva")) reset();
    if (event.target.closest("[data-cerca-azzera]")) {
      reset();
      field.focus();
    }
  });
  root.classList.add("cerca-viva");
  if (field.value) apply(); // a value the browser restored (the back-forward cache, a reload)
  arrive();
  addEventListener("hashchange", arrive);
}
