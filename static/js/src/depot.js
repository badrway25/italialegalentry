/**
 * The Dépôt — the deposit of a file (design V5, W3-C; docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5 item 5;
 * DOCUMENT_WORKSPACE.md §11): templates/documents/partials/depot.html, made a little more than a form.
 *
 * Without this module the Dépôt is complete: the browser's own file control, a real form post, the server's answer as
 * a page — with script but before this module (late, or lost), the frame keeps its drawing and a chosen file shows the
 * browser's own control in it (_depot.css §2 bis), and a file chosen meanwhile is taken up when it arrives. With it,
 * the SAME form goes to the SAME endpoint (apps/documents/views.py, header `X-ILE-Depot`), and the
 * server's answer — one of the eleven of §11.1 — is composed IN PLACE:
 *
 *   ready        a file is chosen and nothing is sent: its whole name in its own order, its type and size; choosing and
 *                sending are two acts (§11.3 rule 1) — the zone stays, a press chooses another file
 *   client guard empty, over the size, outside the allow-list (the server's rules, read from the form: depot.html writes
 *                documents.presenters.deposit_rules) — the file keeps its row and its reason, nothing is sent; a
 *                validity date already past is refused under its field, as a courtesy (the server's clock decides)
 *   transfer     a real <progress> and its share, «Annuler» beside it; the submit's busy key (L2 of «Lume»)
 *   refused      the server's refusal (content, image, active PDF, antivirus) stays on the file's row: its sentence,
 *                verbatim — never a toast alone, never a page change; the zone is the one way on: another file
 *   throttled    the sentence in a notice, in place; the file stays chosen and «Déposer» is the retry
 *   gate         the Conditions: the form gives way to the sentence and its link
 *   filed        the piece is read again (its state changed) and the answer lands under that state, with the filed
 *                state's own mark drawing itself — «filed ≠ examined»: no verdict, no check; on the loose road the
 *                answer names the file before the server's sentence and the zone is back for another file
 *   error        the network, or the server's own failure: its sentence, «Déposer» kept
 * An answer that is not the Dépôt's (a login page after the session ended, a refusal page) reloads the page: the
 * server decides where the person stands — nothing is ever sent twice behind their back.
 *
 * Two live regions, made once and kept outside whatever a refresh replaces, carry the announcements — at the start
 * (the chosen file) and at the end (the answer), assertive for a refusal (§11.2); a new choice or a send empties both
 * first, so neither keeps a sentence that no longer holds. The composed blocks themselves are not live: nothing is
 * read twice. Every word is the page's: the server's sentences, the form's data-* sentences and
 * the <template>s of depot.html. CSP: no inline style, no string evaluated; motion is CSS on the person's act only
 * (the filed mark, _depot.css), still under reduced motion.
 *
 *   initDepots(root = document, { live, refresh })   wires every un-wired Dépôt inside root; idempotent
 *     live      the element that hosts the two live regions (default <body>; the preview drawer passes its panel, so
 *               an announcement is not outside a modal sheet)
 *     refresh   async (depot) → the piece's element read again, or null — default: the page's own piece, fetched
 *               and swapped (the preview drawer passes its body's and the register's)
 */
/** L2 of «Lume» (static/js/src/loader.js) is never imported statically — shell.js loads it on demand (W1-D): a Dépôt
 *  asks for it once it is wired, so it is there by the time a file is sent; its calls keep their order (one promise). */
let loaderModule = null;
const loader = () => (loaderModule ||= import("./loader.js"));

const READY = "depotReady";
const lang = (document.documentElement.lang || "fr").toLowerCase();
const locale = lang.startsWith("ar") ? `${lang}-u-nu-latn` : lang; // Western digits on an Arabic page, as its dates
const TYPES = { ".pdf": "PDF", ".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG" };
let guarded = false; // the window-level drop guard, installed once

/* ---- small helpers -------------------------------------------------------------------------------------------- */

/** The extension as the server reads it (services.sanitise_filename, then extension_of): NFKC, no control
 *  characters, a conservative set, trailing dots, spaces and underscores trimmed — so the courtesy never refuses
 *  what the server would accept. */
function extensionOf(name) {
  const base = String(name || "")
    .normalize("NFKC")
    .replace(/[\u0000-\u001f\u007f]/g, "")
    .replace(/[^\p{L}\p{N}_.\- ]+/gu, "_")
    .replace(/^[ ._]+|[ ._]+$/g, "");
  const dot = base.lastIndexOf(".");
  return dot > 0 && dot < base.length - 1 ? base.slice(dot).toLowerCase() : "";
}

/** A file's size, never a figure that contradicts its refusal (REVIEW m6): an empty file reads «0 ko», not «1 ko»;
 *  from a megabyte one decimal, rounded away from the limit (`max`) — a file over it never reads as the limit itself
 *  («10,1 Mo», not «10 Mo»), one under it never reads over it. */
function sizeOf(bytes, max = 0) {
  const unit = (value, name, digits) =>
    new Intl.NumberFormat(locale, { style: "unit", unit: name, unitDisplay: "short", maximumFractionDigits: digits }).format(value);
  const mega = 1024 * 1024;
  if (bytes >= mega) {
    const tenths = (bytes / mega) * 10;
    return unit((max && bytes > max ? Math.ceil(tenths) : Math.floor(tenths)) / 10, "megabyte", 1);
  }
  return unit(bytes ? Math.max(1, Math.round(bytes / 1024)) : 0, "kilobyte", 0);
}

const percentOf = (share) => new Intl.NumberFormat(locale, { style: "percent", maximumFractionDigits: 0 }).format(share);

/** The file's type and size, each in its own direction (an Arabic size beside a Latin type keeps its reading order). */
function showMeta(element, parts) {
  const nodes = [];
  parts.forEach((part, index) => {
    if (index) nodes.push(document.createTextNode(" · "));
    const span = document.createElement("span");
    span.dir = "auto";
    span.textContent = part;
    nodes.push(span);
  });
  element.replaceChildren(...nodes);
}

/** A <template data-depot-block> of this Dépôt, cloned; a notice from it is not a live region (the regions speak). */
function block(depot, name) {
  const source = depot.querySelector(`template[data-depot-block="${name}"]`);
  if (!source) return null;
  const node = source.content.firstElementChild.cloneNode(true);
  node.removeAttribute("role");
  return node;
}

/** The two live regions of a host, made once: polite (the chosen file, a filing, the throttle) and assertive (a
 *  refusal, an error). */
function regions(host) {
  const make = (kind, role) => {
    let region = host.querySelector(`:scope > [data-depot-live="${kind}"]`);
    if (!region) {
      region = document.createElement("p");
      region.className = "visually-hidden";
      region.setAttribute("role", role);
      region.dataset.depotLive = kind;
      host.append(region);
    }
    return region;
  };
  return { polite: make("polite", "status"), assertive: make("assertive", "alert") };
}

/** The same sentence twice is still read twice: the region is emptied, then given its words a moment later — a timer,
 *  not a frame (an announcement is no motion; a frame is waited on through motion.js only), the latest words winning. */
const SAY_AFTER = 100;
const saying = new WeakMap();
function say(live, text, assertive = false) {
  const region = assertive ? live.assertive : live.polite;
  window.clearTimeout(saying.get(region));
  region.textContent = "";
  saying.set(
    region,
    window.setTimeout(() => {
      region.textContent = text;
    }, SAY_AFTER),
  );
}

/** Both regions emptied, their pending words dropped: a new choice or a new send starts from silence, so a reader who
 *  walks the page never meets the previous file's sentence beside a refusal of the new one (A11Y_PERF a1, W4-C). */
function hush(live) {
  [live.polite, live.assertive].forEach((region) => {
    window.clearTimeout(saying.get(region));
    region.textContent = "";
  });
}

function describe(control, id, on) {
  const ids = new Set((control.getAttribute("aria-describedby") || "").split(/\s+/).filter(Boolean));
  if (on) ids.add(id);
  else ids.delete(id);
  if (ids.size) control.setAttribute("aria-describedby", [...ids].join(" "));
  else control.removeAttribute("aria-describedby");
}

/** A refusal of the chosen file, on its row: the reason in place — and the field marked in error, described by that
 *  reason, as every field in error is (W1-C's grammar; A11Y_PERF finding 4): a reader who leaves the field and comes
 *  back hears why. `clear` in wire() takes both back, and a new choice clears first. */
function refuseFile(depot, text) {
  const row = depot.querySelector("[data-depot-file]");
  const refusal = depot.querySelector("[data-depot-refusal]");
  const input = depot.querySelector('input[type="file"]');
  if (!row || !refusal) return;
  row.hidden = false;
  row.dataset.state = "refused";
  depot.querySelector("[data-depot-refusal-text]").textContent = text;
  refusal.hidden = false;
  if (input) {
    input.setAttribute("aria-invalid", "true");
    if (refusal.id) describe(input, refusal.id, true);
  }
}

/** A field's error in W1-C's grammar (components/form_field.html): the wrapper's error state, the control's
 *  `aria-invalid` and its description, the list under the help. */
function fieldError(control, message) {
  const wrap = control.closest(".form-field");
  if (!wrap) return;
  const id = `${control.id}_error`;
  let box = wrap.querySelector(":scope > .form-field__errors");
  if (!box) {
    box = document.createElement("div");
    box.className = "form-field__errors";
    box.id = id;
    const file = wrap.querySelector(":scope > [data-depot-file]");
    wrap.insertBefore(box, file || null);
  }
  box.removeAttribute("role");
  const list = document.createElement("ul");
  list.className = "form-field__error-list";
  const item = document.createElement("li");
  item.textContent = message;
  list.append(item);
  box.replaceChildren(list);
  wrap.classList.add("form-field--error");
  control.setAttribute("aria-invalid", "true");
  describe(control, box.id, true);
}

/** Every field error inside `scope` — a form, or one field's wrapper — is lifted: the server's from a page drawn
 *  with errors, and the ones composed here. */
function clearFieldErrors(scope) {
  const wraps = scope.matches(".form-field") ? [scope] : [...scope.querySelectorAll(".form-field--error")];
  wraps.forEach((wrap) => {
    wrap.classList.remove("form-field--error");
    wrap.querySelectorAll(":scope > .form-field__errors").forEach((box) => {
      wrap.querySelectorAll("[aria-invalid]").forEach((control) => {
        control.removeAttribute("aria-invalid");
        describe(control, box.id, false);
      });
      box.remove();
    });
  });
}

/* ---- the page's own refresh ------------------------------------------------------------------------------------- */

/** The piece read again after an answer that changed it (a filing; an antivirus refusal, which records a version):
 *  its URL fetched, its <article> swapped for the fresh one. Null when it cannot be read — the page then reloads. */
async function refreshPage(depot) {
  const article = depot.closest("article.doc-piece");
  const url = depot.dataset.depotPiece;
  if (!article || !url) return null;
  try {
    const response = await fetch(url, { credentials: "same-origin", headers: { Accept: "text/html" } });
    if (!response.ok) throw new Error(String(response.status));
    const doc = new DOMParser().parseFromString(await response.text(), "text/html");
    const fresh = doc.querySelector("article.doc-piece");
    if (!fresh) throw new Error("no piece");
    const node = document.importNode(fresh, true);
    article.replaceWith(node);
    return node;
  } catch {
    window.location.reload();
    return null;
  }
}

/* ---- one Dépôt ------------------------------------------------------------------------------------------------- */

function wire(form, options) {
  const depot = form.closest("[data-depot]");
  const input = form.querySelector('input[type="file"]');
  if (!depot || !input) return;
  form.dataset[READY] = "";
  depot.dataset.enhanced = "";
  loader();

  const live = regions(options.live || document.body);
  const refresh = options.refresh || refreshPage;
  const zone = depot.querySelector("[data-depot-zone]");
  const row = depot.querySelector("[data-depot-file]");
  const name = depot.querySelector("[data-depot-name]");
  const meta = depot.querySelector("[data-depot-meta]");
  const transfer = depot.querySelector("[data-depot-transfer]");
  const progress = depot.querySelector("[data-depot-progress]");
  const percent = depot.querySelector("[data-depot-percent]");
  const abort = depot.querySelector("[data-depot-abort]");
  const refusal = depot.querySelector("[data-depot-refusal]");
  const answer = depot.querySelector("[data-depot-answer]");
  const submit = form.querySelector("[data-depot-submit]");
  const note = depot.querySelector(".doc-depot__note");
  const date = form.querySelector('input[type="date"]');
  const rules = form.dataset;
  const max = Number(rules.depotMax) || 0;
  const allowed = (rules.depotExtensions || "").split(",").filter(Boolean);
  const piece = Boolean(depot.dataset.depotPiece);
  let xhr = null;

  if (date && rules.depotToday) date.min = rules.depotToday; // the picker greys the days already past

  /** The server's rules, repeated: the sentence of the first that refuses this file, or "". */
  const guard = (file) => {
    if (!file.size) return rules.depotEmpty || "";
    if (max && file.size > max) return rules.depotTooLarge || "";
    if (allowed.length && !allowed.includes(extensionOf(file.name))) return rules.depotExtension || "";
    return "";
  };
  const partsOf = (file) => [TYPES[extensionOf(file.name)] || "", sizeOf(file.size, max)].filter(Boolean);
  const metaOf = (file) => partsOf(file).join(" · ");

  const clear = () => {
    clearFieldErrors(form);
    if (refusal) {
      refusal.hidden = true;
      if (refusal.id) describe(input, refusal.id, false);
    }
    input.removeAttribute("aria-invalid");
    if (row) delete row.dataset.state;
    if (answer) answer.replaceChildren();
    hush(live);
  };
  const showFile = (file) => {
    if (!row) return;
    name.textContent = file.name;
    showMeta(meta, partsOf(file));
    row.hidden = false;
  };
  const refuse = (text) => refuseFile(depot, text);
  /** The controls wait with the transfer (the form data is read before); a file's transfer shows its progress. */
  const controls = () => form.querySelectorAll("input:not([type=hidden]), select, textarea");
  const sending = (withFile) => {
    // a control about to wait drops the focus to the page: it goes first to the act that is waiting
    if (form.contains(document.activeElement) && document.activeElement !== submit) submit.focus();
    controls().forEach((control) => {
      control.disabled = true;
    });
    if (zone) zone.setAttribute("data-sending", ""); // the frame waits with its field (_depot.css)
    if (!withFile) return;
    if (progress) progress.value = 0;
    if (percent) percent.textContent = "";
    if (transfer) transfer.hidden = false;
    if (abort) abort.hidden = false;
  };
  const notice = (kind, text, assertive) => {
    const node = block(depot, kind);
    if (!node || !answer) return;
    if (text) {
      const body = node.querySelector(".notice__body");
      if (body) body.textContent = text;
    }
    answer.replaceChildren(node);
    const words = [node.querySelector(".notice__title"), node.querySelector(".notice__body")]
      .filter(Boolean)
      .map((part) => part.textContent.replace(/\s+/g, " ").trim());
    say(live, words.join(". "), assertive);
  };

  /* the zone: a file held above it lights it; the input under the pointer takes the drop itself */
  if (zone) {
    let depth = 0;
    const hasFiles = (event) => [...(event.dataTransfer?.types || [])].includes("Files");
    zone.addEventListener("dragenter", (event) => {
      if (!hasFiles(event)) return;
      depth += 1;
      zone.classList.add("is-over");
    });
    zone.addEventListener("dragleave", () => {
      depth = Math.max(0, depth - 1);
      if (!depth) zone.classList.remove("is-over");
    });
    zone.addEventListener("drop", () => {
      depth = 0;
      zone.classList.remove("is-over");
    });
  }

  /* ready — or refused by the client guard: the file keeps its row and its reason */
  input.addEventListener("change", () => {
    clear();
    const file = input.files && input.files[0];
    if (!file) {
      if (row) row.hidden = true;
      return;
    }
    showFile(file);
    const reason = guard(file);
    if (reason) {
      refuse(reason);
      say(live, reason, true);
    } else {
      say(live, `${file.name} — ${metaOf(file)}`);
    }
  });

  /* a validity date already past: refused under its own field, the file still chosen */
  const datePast = () => Boolean(date && date.value && rules.depotToday && date.value < rules.depotToday);
  if (date) {
    date.addEventListener("change", () => {
      const wrap = date.closest(".form-field");
      if (wrap) clearFieldErrors(wrap);
      if (datePast()) {
        fieldError(date, rules.depotPast);
        say(live, rules.depotPast, true);
      }
    });
  }

  if (abort) abort.addEventListener("click", () => xhr && xhr.abort());

  form.addEventListener("submit", (event) => {
    // the Dépôt answers in the page: the submit is refused here, before shell.js's hook gives the busy face itself
    event.preventDefault();
    if (xhr) return;
    const file = input.files && input.files[0];
    const reason = file ? guard(file) : "";
    if (reason) {
      clear();
      showFile(file);
      refuse(reason);
      say(live, reason, true);
      input.focus();
      return;
    }
    if (datePast()) {
      clearFieldErrors(form);
      fieldError(date, rules.depotPast);
      say(live, rules.depotPast, true);
      date.focus();
      return;
    }
    clear();
    send(file);
  });

  // a file chosen before this module arrived — the frame showed the browser's own control meanwhile (_depot.css §2 bis)
  // — is shown, guarded and said now, as if chosen this moment (W4-C's review, M2)
  if (input.files && input.files.length) input.dispatchEvent(new Event("change"));

  function send(file) {
    const data = new FormData(form); // read before the controls are disabled
    xhr = new XMLHttpRequest();
    xhr.open("POST", form.action);
    xhr.setRequestHeader("X-ILE-Depot", "1");
    xhr.setRequestHeader("Accept", "application/json");
    loader().then(({ busy }) => busy(submit));
    sending(Boolean(file));
    xhr.upload.addEventListener("progress", (event) => {
      if (!event.lengthComputable || !progress) return;
      const share = event.loaded / event.total;
      progress.value = Math.round(share * 100);
      if (percent) percent.textContent = percentOf(share);
    });
    xhr.addEventListener("load", () => {
      const request = xhr;
      xhr = null;
      answered(request, file);
    });
    xhr.addEventListener("error", () => {
      xhr = null;
      over(true);
      notice("error", "", true);
    });
    xhr.addEventListener("abort", () => {
      xhr = null;
      over(true);
      submit.focus(); // «Annuler» has left with the transfer: the focus goes to the act that sends again
    });
    xhr.send(data);
  }

  /** The wait is over: the controls are back, the transfer row folds, the key rests (lit when an answer came). */
  function over(quietly) {
    controls().forEach((control) => {
      control.disabled = false;
    });
    if (zone) zone.removeAttribute("data-sending");
    if (transfer) transfer.hidden = true;
    if (abort) abort.hidden = true;
    loader().then(({ rest, settle }) => (quietly ? rest(submit) : settle(submit)));
  }

  async function answered(request, file) {
    let body = null;
    if ((request.getResponseHeader("Content-Type") || "").includes("application/json")) {
      try {
        body = JSON.parse(request.responseText);
      } catch {
        body = null;
      }
    }
    if (!body || typeof body.answer !== "string") {
      over(true);
      if (request.status >= 500) notice("server", "", true);
      else window.location.reload(); // not the Dépôt's answer: the server decides where the person stands
      return;
    }
    const message = String(body.message || "");
    switch (body.answer) {
      case "filed":
      case "infected":
        await changed(body.answer, message, file);
        return;
      case "throttled":
        over(false);
        notice("throttled", "", false);
        return;
      case "terms":
        over(true);
        gate(message);
        return;
      default:
        over(false);
        refused(body, message, file);
    }
  }

  /** A refusal of the form (422): on the file's row, under the field it names, or as a notice. */
  function refused(body, message, file) {
    const field = body.field ? form.elements.namedItem(body.field) : null;
    if (body.field === input.name && file) {
      showFile(file);
      refuse(message);
      say(live, message, true);
      input.focus();
    } else if (field && field.nodeType === 1) {
      fieldError(field, message);
      say(live, message, true);
      field.focus();
    } else {
      notice("error", message, true);
    }
  }

  /** The Conditions gate: the form gives way to the gate's sentence and its link. */
  function gate(message) {
    const node = block(depot, "gate");
    if (!node) return;
    const text = node.querySelector("[data-depot-gate-text]");
    if (text) text.textContent = message;
    form.replaceWith(node);
    if (note) note.hidden = true; // the formats are said for a field there no longer is
    say(live, message, true);
    const link = node.querySelector("a");
    (link || node).focus();
  }

  /** An answer that changed the piece (a filing; an antivirus refusal, which records a version): the piece is read
   *  again, and the answer lands in the fresh one — under its state for a filing, on the fresh Dépôt's file row for a
   *  refusal. A loose file changes no piece: its answer stays in this Dépôt. */
  async function changed(kind, message, file) {
    if (!piece) {
      over(false);
      if (kind === "infected") {
        showFile(file);
        refuse(message);
        say(live, message, true);
        return;
      }
      const node = block(depot, "filed");
      if (node) {
        const named = node.querySelector("[data-depot-filed-name]");
        if (named && file) {
          named.textContent = file.name;
          named.hidden = false;
        }
        node.querySelector("[data-depot-filed-text]").textContent = message;
        node.setAttribute("tabindex", "-1");
        // the Dépôt stays for the next file (REVIEW m5): the form set back, the answer in its slot until a new choice
        form.reset();
        if (row) row.hidden = true;
        if (answer) answer.replaceChildren(node);
        else form.after(node);
        say(live, file ? `${file.name} — ${message}` : message);
        node.focus();
      }
      return;
    }
    const filedBlock = block(depot, "filed");
    over(false);
    const fresh = await refresh(depot);
    if (!fresh) return;
    initDepots(fresh, options);
    if (kind === "filed") {
      const slot = fresh.querySelector("[data-piece-answer]");
      if (slot && filedBlock) {
        filedBlock.querySelector("[data-depot-filed-text]").textContent = message;
        slot.replaceChildren(filedBlock);
      }
      say(live, message);
      const heading = fresh.querySelector(".doc-piece__state .doc-piece__h2");
      if (heading) {
        heading.setAttribute("tabindex", "-1");
        heading.focus();
      }
      return;
    }
    // the antivirus kept nothing: the piece is NOT VALID now, and open — its fresh Dépôt says why, on the file's row
    const next = fresh.querySelector("[data-depot]");
    const nextRow = next && next.querySelector("[data-depot-file]");
    if (nextRow && file) {
      next.querySelector("[data-depot-name]").textContent = file.name;
      showMeta(next.querySelector("[data-depot-meta]"), partsOf(file));
      refuseFile(next, message);
      const nextInput = next.querySelector('input[type="file"]');
      if (nextInput) nextInput.focus();
    }
    say(live, message, true);
  }
}

/* ---- the drop guard -------------------------------------------------------------------------------------------- */

/** A file dropped beside the zone would make the browser open it and leave the page: refused there, quietly. */
function guardDrops() {
  if (guarded) return;
  guarded = true;
  const outside = (event) =>
    [...(event.dataTransfer?.types || [])].includes("Files") && !(event.target instanceof Element && event.target.closest("[data-depot-zone]"));
  window.addEventListener("dragover", (event) => {
    if (!outside(event)) return;
    event.preventDefault();
    event.dataTransfer.dropEffect = "none";
  });
  window.addEventListener("drop", (event) => {
    if (outside(event)) event.preventDefault();
  });
}

export function initDepots(root = document, options = {}) {
  const forms = [...root.querySelectorAll("form[data-depot-form]")].filter((form) => !(READY in form.dataset));
  forms.forEach((form) => wire(form, options));
  if (forms.length) guardDrops();
}
