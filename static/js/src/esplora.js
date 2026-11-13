/**
 * «L'esploratore» (/parcours/, V5.32 lane B — the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION, 12 Nov 2026).
 * From 64 rem, pointing at a pathway's row or focusing it shows its preview beside the rows (templates/pathways/
 * _esplora.html). The rows stay links to their sheets; nothing is announced (the preview repeats the row for the eye
 * and is hidden from assistive technology). The new preview rises in on transform/opacity (pathways/_esplora.css);
 * under reduced motion it simply appears. Without this module there is no preview: every row shows its line.
 */
const WIDE = window.matchMedia("(min-width: 64rem)");
const INTENT_MS = 70; // a pointer crossing the list does not flick every preview on its way

function setup(root) {
  const rows = [...root.querySelectorAll("[data-esplora-voce]")];
  const cards = new Map([...root.querySelectorAll("[data-esplora-anteprima]")].map((c) => [c.dataset.esploraAnteprima, c]));
  if (!rows.length || !cards.size) return;
  let current = rows[0].dataset.esploraVoce;
  let timer = 0;

  const show = (key) => {
    if (key === current || !cards.has(key)) return;
    cards.get(current)?.setAttribute("hidden", "");
    const card = cards.get(key);
    card.removeAttribute("hidden");
    card.classList.remove("is-entering");
    void card.offsetWidth; // restart the entrance
    card.classList.add("is-entering");
    current = key;
    rows.forEach((row) => row.toggleAttribute("data-attiva", row.dataset.esploraVoce === key));
  };

  rows.forEach((row) => {
    const key = row.dataset.esploraVoce;
    row.addEventListener("pointerenter", () => {
      if (!WIDE.matches) return;
      clearTimeout(timer);
      timer = setTimeout(() => show(key), INTENT_MS);
    });
    row.addEventListener("pointerleave", () => clearTimeout(timer));
    row.addEventListener("focus", () => WIDE.matches && show(key));
  });
  rows[0].toggleAttribute("data-attiva", true);
  root.setAttribute("data-esplora-pronto", "");
}

document.querySelectorAll("[data-esplora]").forEach(setup);
