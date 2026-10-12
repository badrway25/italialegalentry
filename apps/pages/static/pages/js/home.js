/*
 * Homepage — progressive enhancement only (the page is complete without this file).
 *
 * Dismissible institutional notice: `[data-dismissible="<id>"]` wrappers hold a hidden
 * `[data-dismiss]` button. With JS the button appears; activating it hides the notice and
 * remembers the choice for the current tab in sessionStorage — no cookie, no identifier, nothing
 * sent to the server. Focus moves to the main landmark so keyboard users are never left on a
 * removed control.
 */
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
