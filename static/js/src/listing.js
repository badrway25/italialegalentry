/**
 * The platform's list toolkit — the enhancements of the bar and of the drawer's form (V5.30, stream C;
 * docs/design-v5/QA/v530/plat/NOTES.md §1). Markup: templates/components/listing/{toolbar,filters}.html; the drawer is
 * the overlay system's (static/js/src/overlay.js, wired by console.js on every console page); the server reads and
 * checks every parameter (apps/portal/listing.py).
 *
 * Without this module every part already works: the bar and the drawer are GET forms, a chip is a link, «Tout effacer»
 * a link, and a sort chosen applies with the search's submit. It adds, on native APIs only:
 *   · the sort applies as soon as it is chosen (`change` → requestSubmit(), which runs the form's own submit path);
 *   · a form leaves its empty fields — and the default order — out of the address: they are disabled for the length of
 *     the submit, and given back if the page comes back from the back-forward cache; the URL holds only what narrows.
 * No word, no style, no markup is written here (CSP `script-src 'self'`; nothing evaluated, nothing inserted).
 */
for (const select of document.querySelectorAll("[data-listing-sort]")) {
  select.addEventListener("change", () => select.form && select.form.requestSubmit());
}

for (const form of document.querySelectorAll("[data-listing-form]")) {
  form.addEventListener("submit", () => {
    const quiet = [...form.elements].filter(
      (field) =>
        field.name &&
        !field.disabled &&
        ((field.value === "" && (field.type !== "radio" || field.checked)) ||
          // the default order (the sort's first option) is the list as it opens: not a criterion
          (field.matches("[data-listing-sort]") && field.selectedIndex === 0)),
    );
    quiet.forEach((field) => {
      field.disabled = true;
    });
    window.addEventListener("pageshow", () => quiet.forEach((field) => (field.disabled = false)), { once: true });
  });
}
