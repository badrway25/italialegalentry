// Orientation wizard — progressive enhancement only. Everything works without this file.
// * reveals the print button (needs JS)
// * after an HTMX swap, moves focus to the new question so keyboard/screen-reader users stay oriented

const focusQuestion = (root) => {
  const target = (root || document).querySelector("#wizard-question");
  if (target) {
    target.focus({ preventScroll: false });
  }
};

document.querySelectorAll(".js-print").forEach((button) => {
  button.hidden = false;
  button.addEventListener("click", () => window.print());
});

document.body.addEventListener("htmx:afterSwap", (event) => {
  if (event.target && event.target.id === "orientation-step") {
    focusQuestion(event.target);
  }
});

document.body.addEventListener("htmx:responseError", () => {
  // Fall back to a full page load if the partial swap fails.
  window.location.reload();
});
