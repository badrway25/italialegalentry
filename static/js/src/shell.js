/**
 * Shell behaviour shared by every public page — the one public entry (docs/design-v5/V5_4_EXECUTION_PLAN.md
 * §2.3): it imports the navigation and adds the few behaviours every page shares.
 *
 *   overlay.js             the overlay system (W2-A; plan §1.14), imported here for every public page (W2-C2, plan
 *                          §2.3): it wires its hooks when it loads — the sheet below 80rem, the signed-in targa's
 *                          account popover, the tooltip of the key alone; the console's console.js imports the same
 *                          module, one chunk for both
 *   nav.js                 «Il portico» (W2-C1, W2-C2): the letterhead's scrolled state, the bar and its door panels,
 *                          «l'architrave», the keyboard model, the sheet's one rule of its own. It replaces this
 *                          file's V4 header observer and sliding indicator, and main.js's initNavigation.
 *   [data-password-toggle] fields that show and hide themselves (design V4 §3.3; the glyph control, the kept
 *                          caret and no spelling on a shown password: design V5 «Il varco», W2-B)
 *   form (submit)          a submitted form's button waits — L2 of the loader «Lume» (W1-D): `aria-busy`, and the
 *                          busy key where it has a place; the state machine is loader.js, imported on the first
 *                          submit and never before
 *
 * No animation is written here — the busy key is a class, which v5/loader.css turns. The reveal of design V2
 * ([data-reveal], the Motion library's inView + animate + stagger) left with W4-B: text never waits for a reveal
 * (V5.4 plan §1.5 K17), and no page carried the attribute any more.
 */
import "./overlay.js";
import { initNavigation } from "./nav.js";

initNavigation();

/* 3. Password fields show and hide themselves (design V4 §3.3; W1-C, review M2 and A10): a glyph in the
      plate's end swaps the input's type; its name is constant and aria-pressed is the one channel of the
      state — v5/field.css swaps the eye on it. Nothing is submitted, nothing is stored.
      · THE CARET IS KEPT (design V5 «Il varco», V5.4 plan §1.13; W2-B): a pointer's press hands the focus
        back to the field with its selection as it was, so the person goes on typing where they were;
        pressed from the keyboard, the control keeps the focus — it can be pressed again, and its state is
        read from it.
      · A SHOWN PASSWORD IS STILL A SECRET (W2-B, review M2): shown, the field is a text field, and a text
        field is spell-checked — by a vendor's spelling service where the browser has one — capitalised and
        corrected by a phone's keyboard. Every field this control can show is told not to, once, when the
        control is wired: every revealable password of the site, the sign-up's and the new password's too.
        Without script there is no control, and a password field is never spell-checked. */
document.querySelectorAll("[data-password-toggle]").forEach((button) => {
  const input = document.getElementById(button.getAttribute("aria-controls"));
  if (!input) return;
  input.spellcheck = false;
  input.setAttribute("autocapitalize", "none");
  input.setAttribute("autocorrect", "off");
  button.addEventListener("click", (event) => {
    const shown = input.type === "text";
    const { selectionStart, selectionEnd, selectionDirection } = input;
    input.type = shown ? "password" : "text";
    button.setAttribute("aria-pressed", shown ? "false" : "true");
    if (event.detail === 0) return; // a press from the keyboard (or by a script): the focus stays on the control
    input.focus({ preventScroll: true });
    input.setSelectionRange(selectionStart, selectionEnd, selectionDirection);
  });
});

/* 4. A submitted form's control waits until the answer replaces the page — L2 of the loader «Lume»
      (V5.4 plan §1.9, W1-D): v5/loader.css draws the key on `.btn.is-busy` and turns it once; `aria-busy`
      tells assistive technology why nothing happens. Both are set here, in the submit's own task, so
      the busy face is in the click's frame; the rest of the state machine — `aria-disabled` where the
      second submit is refused, the lease that ends the wait, the words of a long wait, the engage of a
      sign-in's stage (`data-loader-host`) — is static/js/src/loader.js, imported on the first submit and
      never before (plan §2.3: the loader loads through shell.js). A submit another script refused
      (main.js's double-submit guard) changes nothing.
      A WAIT THAT NOTHING WOULD END IS NEVER DECLARED (the review-once of V5.5, 9 October 2026):
      · the wait is for an answer that replaces THIS page. A form whose answer is a file says so with
        `data-loader="none"` (the account's «Exporter mes données (JSON)»: the page stays, and no event
        tells a script that a download began); a form that opens elsewhere (`target`) or only closes a
        dialog (`method="dialog"`) is read from its own markup. Nothing is set, nothing is loaded;
      · only a `.btn` waits — the control v5/loader.css knows. A submit control that is not a button of
        the system (the account menu's logout) declares no `aria-busy` the eye cannot see;
      · the key only where it has a place: it sits in a button's inline-end padding, and a link-styled or
        icon-only button has none (KEYLESS) — the key would be drawn over the label's last glyphs. Such a
        control says `aria-busy` and keeps its own face: no class, so neither the key nor V4's busy slab;
      · a page that comes back from the back/forward cache comes back as it was left: every control this
        hook marked is at rest again, whether or not loader.js had arrived (`faced`, `pageshow`);
      · if loader.js cannot be loaded there is no state machine, so nothing waits — and nothing refuses: main.js's
        double-submit guard on a `data-single-submit` form (the mark, the `aria-disabled` of its submit buttons) is
        lifted with the face, at once — the lease that would have lifted it later is loader.js's, and it is not
        there: a refusal that nothing would end is never left announced (WCAG 4.1.3; the account's profile form is
        guarded since W3-F2). */
const faced = new Set(); // the controls this hook has marked since the page was shown
let returns = 0; // the returns from the cache so far: a submit from before one is over
/** The `.btn` variants with no inline padding (v5/buttons.css: `--btn-pad: 0`): their box is their text or their
    icon. tests/frontend/test_loader_rules.py reads this list against the sheets. */
const KEYLESS = ".btn--link, .btn--text, .btn--icon";

const restFace = (control) => {
  control.classList.remove("is-busy", "is-lit");
  control.removeAttribute("aria-busy");
  faced.delete(control);
};

/** Does the form's own markup say that its answer will not replace this page? */
const staysOnPage = (form, submitter) => {
  if (form.dataset.loader === "none") return true;
  const own = (name) => (submitter && submitter.getAttribute(`form${name}`)) || form.getAttribute(name) || "";
  return own("method").toLowerCase() === "dialog" || !["", "_self"].includes(own("target"));
};

document.addEventListener("submit", (event) => {
  const form = event.target;
  if (!(form instanceof HTMLFormElement) || event.defaultPrevented) return;
  // the control that was pressed; a form sent with no submitter (requestSubmit()) falls back on its default button
  const submitter = event.submitter || form.querySelector('button[type="submit"], button:not([type])');
  if (staysOnPage(form, submitter)) return;
  // a <button>: an <input type="submit"> has no ::after for the key, and it is never another control's wait
  const control = submitter instanceof HTMLButtonElement && submitter.classList.contains("btn") ? submitter : null;
  if (control) {
    if (!control.matches(KEYLESS)) control.classList.add("is-busy");
    control.setAttribute("aria-busy", "true");
    faced.add(control);
  }
  if (!control && !form.dataset.loaderHost) return; // nothing waits, nothing to engage: nothing to load
  const at = returns;
  import("./loader.js")
    .then((loader) => {
      if (at === returns) loader.submitted(form, control, event);
    })
    .catch(() => {
      if (control) restFace(control);
      if (!form.hasAttribute("data-single-submit")) return;
      form.removeAttribute("data-submitted");
      form.querySelectorAll('button[type="submit"]').forEach((button) => button.removeAttribute("aria-disabled"));
    });
});

window.addEventListener("pageshow", (event) => {
  if (!event.persisted) return;
  returns += 1;
  [...faced].forEach(restFace);
});
