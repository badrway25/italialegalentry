/**
 * «Lo sportello» — the contact page's copy action (V5.32, lane D; after 21st.dev «Contact Page», efferd id 7139: the
 * address with a copy-to-clipboard action — adapted, not copied). Progressive enhancement: the button is `hidden` in
 * the markup and shown only where the Clipboard API exists; without it the address stays a mailto link to select.
 *
 * Markup (templates/pages/contact.html):
 *   [data-copia="<id>"]        the button; <id> is the element whose text is copied;
 *   [data-copia-fatto]         its «copied» sentence (the page's own words, in the page's language);
 *   [data-copia-testo]         the button's visible words, swapped for 2 s;
 *   [data-copia-stato]         a role=status sibling that says the result to assistive technology.
 * No word is written by this module.
 */
for (const button of document.querySelectorAll("[data-copia]")) {
  const source = document.getElementById(button.dataset.copia);
  if (!source || !navigator.clipboard || !window.isSecureContext) continue;
  const words = button.querySelector("[data-copia-testo]");
  const status = button.parentElement.querySelector("[data-copia-stato]");
  const rest = words ? words.textContent : "";
  let timer = 0;
  button.hidden = false;
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(source.textContent.trim());
    } catch {
      return;
    }
    const done = button.dataset.copiaFatto || "";
    button.dataset.copiato = "";
    if (words) words.textContent = done;
    if (status) status.textContent = done;
    clearTimeout(timer);
    timer = setTimeout(() => {
      delete button.dataset.copiato;
      if (words) words.textContent = rest;
      if (status) status.textContent = "";
    }, 2000);
  });
}
