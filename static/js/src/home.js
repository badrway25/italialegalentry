/**
 * The home's one entry (design V5.4, plan §2.3 «JavaScript»; W2-D): it imports the hero's module and carries the
 * dismissible institutional notice — moved verbatim from apps/pages/static/pages/js/home.js, which is deleted (one
 * request fewer). Bundled by esbuild into static/js/dist/home.js and loaded by templates/pages/home.html as a module:
 * deferred, never inline.
 *
 * The V4 hero's choreography (the route anchoring, the scroll-linked photograph and stage, the legend's hover state)
 * left with the V4 hero: the V5 hero is hero.js, and its hand states are CSS (hero.css). The pilot route's line, drawn
 * with the scroll, left with the route (W2-D step 3): the Morocco → Italy model is said once, by the hero's path, and
 * the chapters under the hero do not move.
 */
import "./hero.js";

/* THE DISMISSIBLE NOTICE — progressive enhancement only (the page is complete without it).
      `[data-dismissible="<id>"]` wrappers hold a hidden `[data-dismiss]` button. With JS the button
      appears; activating it hides the notice and remembers the choice for the current tab in
      sessionStorage — no cookie, no identifier, nothing sent to the server. Focus moves to the main
      landmark so keyboard users are never left on a removed control. */
const PREFIX = "ile.dismissed.";

function storage() {
  try {
    const probe = `${PREFIX}probe`;
    window.sessionStorage.setItem(probe, "1");
    window.sessionStorage.removeItem(probe);
    return window.sessionStorage;
  } catch (error) {
    return null; // storage blocked: the notice is simply dismissed for this page view
  }
}

function initDismissible(wrapper, store) {
  const key = PREFIX + wrapper.dataset.dismissible;
  const button = wrapper.querySelector("[data-dismiss]");
  if (!button) return;
  if (store && store.getItem(key) === "1") {
    wrapper.hidden = true;
    return;
  }
  button.hidden = false;
  button.addEventListener("click", () => {
    wrapper.hidden = true;
    if (store) store.setItem(key, "1");
    const main = document.getElementById("main-content");
    if (main) main.focus({ preventScroll: true });
  });
}

const store = storage();
document.querySelectorAll("[data-dismissible]").forEach((wrapper) => initDismissible(wrapper, store));
