/**
 * The region — T4 of the loader «Lume» (V5.12 §4; the Director's DECISIONS §1 T4, §3 «Loading states»: 21st.dev
 * Shapes Skeleton 29863, its static shapes only). A part of a page whose content is on its way says so, only when the
 * wait is real:
 *   · nothing for the first --motion-wait (400 ms: the wait the eye forgives — a fast answer shows nothing);
 *   · then `aria-busy="true"` on the region and `is-busy` on its host — the host draws the busy key in its head (L2's
 *     markup) and, where it has them, its static skeleton shapes (no pulse: nothing loops);
 *   · after WORD_AFTER (1 s) the word, in the region's `role="status"` line (`data-region-word`), said once;
 *   · on arrival, or on failure, every trace is removed at once; seating the rows (L3, loader.js `seat`) is the
 *     caller's, who knows whether the content is new.
 * Reduced motion and the keyboard see the same states: the key's turn is a token (0 ms there), the shapes are still.
 * Imported by piece-drawer.js (the drawer's fetch) and depot.js (the piece read again after a filing); re-exported
 * by loader.js. No word here: the word is the page's.
 */
const WAIT = 400; // --motion-wait
const WORD_AFTER = 1000;

/** Resolves (or rejects) as `promise` does; meanwhile the region says it waits, once the wait is real. */
export function region(container, promise, { host = container, status = null } = {}) {
  if (!container) return Promise.resolve(promise);
  const busy = window.setTimeout(() => {
    container.setAttribute("aria-busy", "true");
    if (host) host.classList.add("is-busy");
  }, WAIT);
  const word = window.setTimeout(() => {
    if (status && status.dataset.regionWord) status.textContent = status.dataset.regionWord;
  }, WORD_AFTER);
  const end = () => {
    window.clearTimeout(busy);
    window.clearTimeout(word);
    container.removeAttribute("aria-busy");
    if (host) host.classList.remove("is-busy");
    if (status) status.textContent = "";
  };
  return Promise.resolve(promise).then(
    (value) => {
      end();
      return value;
    },
    (error) => {
      end();
      throw error;
    },
  );
}
