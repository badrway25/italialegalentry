// Orientation wizard — progressive enhancement only. Everything works without this file.
// * reveals the print button (needs JS)
// * the questionnaire's keyboard model (design V5.4, W3-F1 step 2): every answer is a full post and a new page, so
//   when a step is reached FROM the questionnaire itself — «Commencer» on its first page, «Continuer» or «Précédent»
//   on a step, an answer refused — the focus goes to the new question (the fieldset's legend), not back to the top
//   of the document: Tab then reaches the first choice, and a screen reader reads the question (an error under it
//   is announced by its own role="alert"). A step opened any other way — a link, a bookmark, a reload from
//   elsewhere — keeps the browser's own start.
// * after an HTMX swap (HTMX is not loaded by the project today: a full page load answers), the same.

const focusQuestion = (root) => {
  const target = (root || document).querySelector("#wizard-question");
  if (target) {
    target.focus({ preventScroll: false });
  }
};

// The questionnaire's own pages: its first page (/<lang>/orientation/) and its steps (…/session/<id>/).
const cameFromTheQuestionnaire = () => {
  if (!document.referrer) {
    return false;
  }
  try {
    const previous = new URL(document.referrer);
    const base = window.location.pathname.replace(/session\/.*$/, "");
    return previous.origin === window.location.origin
      && (previous.pathname === base || previous.pathname.startsWith(`${base}session/`));
  } catch {
    return false;
  }
};

document.querySelectorAll(".js-print").forEach((button) => {
  button.hidden = false;
  button.addEventListener("click", () => window.print());
});

if (document.querySelector("#orientation-step") && cameFromTheQuestionnaire()) {
  focusQuestion(document);
}

document.body.addEventListener("htmx:afterSwap", (event) => {
  if (event.target && event.target.id === "orientation-step") {
    focusQuestion(event.target);
  }
});

document.body.addEventListener("htmx:responseError", () => {
  // Fall back to a full page load if the partial swap fails.
  window.location.reload();
});
