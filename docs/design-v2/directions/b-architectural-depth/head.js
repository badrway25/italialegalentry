/* Runs synchronously in <head> (external file: CSP script-src 'self' forbids inline).
   Swaps the no-js class so the stylesheet may hold reveal targets at their initial
   state only when JavaScript will actually run the reveal. Without JS nothing is hidden. */
document.documentElement.classList.replace("no-js", "js");
