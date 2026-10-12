/* V5 live preview — the script of the preview's own pages. DEVELOPMENT ONLY.

   A classic script, outside scripts/build_frontend.mjs and static/js/dist/,
   loaded by templates/dev/designpreview/ alone; it touches no production
   bundle, asks the network for nothing and stores nothing. Every page works
   without it: it only makes three things better.

   1. The archive's pickers (frame.html, compare.html): the keyboard. The bar
      is plain links; this lets the owner press the key each link carries in
      data-dp-key, and says in its title, instead of clicking it. Hero picker:
      0 a b c d e for the variant (the three concept frames E1–E3 of H-E have
      no key), f r for the language, 3 i for the phase. Type picker: v a s p b
      c d for the system, 1 to 5 for the surface, f r for the language.
      Compare view: f r for the language. The keys come from the data, not
      from here. Keys pressed inside a framed comp belong to the comp.

   2. The landing (landing.html): the strip follows the frame. When the page
      in the frame navigates, the strip says that page's state («V5 —
      council-passed» only where the steward's live_status.json says so, from
      the data block the view wrote), its languages, «Apri a parte» and the
      frame links point at it, the persona forms carry it, the frame and the
      window are named after it, and the address bar keeps it (?page=…) so
      that a reload frames it again. It follows every page the landing may
      frame: a page under a language prefix, or one of the documents app
      (map.follow). The frame — the window or a phone of 390 — changes without
      reloading the page.
      Never a blank frame: when the page the frame was asked for cannot be
      shown in it — the back-office, the preview itself, another site — the
      stage says so, with the page alone (when its address is known) and the
      way back (review W1-P B1). After the product's own «Se déconnecter»
      inside the frame, the landing is loaded again, so that the strip stops
      naming a persona whose session is over (review W1-P, UX m9).
      Signed out, on the sign-in, the strip says the way in without a password
      («Personas») and every «Entrer» carries the page the sign-in was asked
      for (its next), so that «Entrer» opens it when it is that persona's own
      (review W1-P, UX r2 n2; CD condition C4).
      And an old link to an anchor of the hub (/__design-v5/#g-…) is sent on
      to the research archive, which holds that anchor now.

   The strip's menus: one open at a time; Escape closes the open one and
   gives the focus back to its summary when the focus was inside it; a click
   elsewhere, the keyboard leaving a menu, or a step into the frame closes
   them. Choosing the frame from «Altro» gives the focus back to «Altro»'s
   summary (review W1-P, accessibility M1, m2).

   3. The index (index.html): its frames, AT MOST ONE PAIR AT A TIME. «Desktop
      1440» and «Telefono 390» of one URL are a pair; opening a frame of
      another URL first unloads the pair that is open — each frame is emptied
      (about:blank) and removed — and only then loads the next. Closing the
      dialog unloads them too, and so does pressing a pressed frame button
      for its own frame. A frame asks the server for its page from one
      pending timer, which an unload cancels: a burst of switches asks for the
      pair that remains, not for every pair on the way (review W1-P,
      performance P-2). The timer waits 150 ms only after an unload that
      removed a frame; a first open, and the second frame of a pair, are
      asked for at the next task (performance r2 P-4; CD condition C7).
      «1:1» acts on the desktop frame, and is disabled while there is none. The preview server has eight database slots; a frame
      is a page and its requests. The desktop frame lays its page out at 1440
      CSS pixels and is drawn scaled to fit beside the phone, «1:1» drawing it
      at its true size (review W1-P M1). Without the script the two links open
      the landing, which holds one frame. */
(function () {
  "use strict";

  var forEach = function (list, callback) {
    Array.prototype.forEach.call(list, callback);
  };

  /* ------------------------------------------------------------------ 1 */
  var bar = document.querySelector("[data-dp-bar]");
  if (bar) {
    var keys = {};
    forEach(bar.querySelectorAll("a[data-dp-key]"), function (link) {
      keys[link.getAttribute("data-dp-key")] = link;
    });
    document.addEventListener("keydown", function (event) {
      if (event.altKey || event.ctrlKey || event.metaKey || event.defaultPrevented) {
        return;
      }
      var target = event.target;
      if (target && (target.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName))) {
        return;
      }
      var link = keys[String(event.key).toLowerCase()];
      if (link && link.href) {
        event.preventDefault();
        window.location.assign(link.href);
      }
    });
  }

  /* ------------------------------------------------------------------ 2 */
  var strip = document.querySelector("[data-dp-strip]");
  var frame = document.querySelector("iframe[data-dp-frame]");
  var stage = document.querySelector("[data-dp-stage]");

  if (strip && /^#g-[a-z0-9-]+$/.test(window.location.hash) && frame) {
    window.location.replace(strip.getAttribute("data-dp-archive") + window.location.hash);
    return;
  }

  if (strip) {
    var menus = strip.querySelectorAll("details");
    var closeMenus = function (except) {
      forEach(menus, function (menu) {
        if (menu !== except) {
          menu.open = false;
        }
      });
    };
    forEach(menus, function (menu) {
      menu.addEventListener("toggle", function () {
        if (menu.open) {
          closeMenus(menu);
        }
      });
      /* The keyboard left the menu: it closes, so that it never covers what the focus reaches next.
         A click on the panel's own words moves the focus nowhere (no related target): it stays open. */
      menu.addEventListener("focusout", function (event) {
        if (menu.open && event.relatedTarget && !menu.contains(event.relatedTarget)) {
          menu.open = false;
        }
      });
    });
    document.addEventListener("keydown", function (event) {
      var open = event.key === "Escape" ? strip.querySelector("details[open]") : null;
      if (open) {
        var inside = open.contains(document.activeElement);
        open.open = false;
        if (inside) {
          open.querySelector("summary").focus();
        }
      }
    });
    document.addEventListener("click", function (event) {
      if (!strip.contains(event.target)) {
        closeMenus(null);
      }
    });
    window.addEventListener("blur", function () {
      window.setTimeout(function () {
        if (document.activeElement && document.activeElement.tagName === "IFRAME") {
          closeMenus(null);
        }
      }, 0);
    });
  }

  function readMap() {
    var block = document.getElementById("dp-live-map");
    if (!block) {
      return null;
    }
    try {
      return JSON.parse(block.textContent);
    } catch (error) {
      return null;
    }
  }

  var map = readMap();
  var prefix = /^\/(it|fr|en|ar)\//;
  var follows = map && map.follow ? new RegExp(map.follow) : prefix;
  /* What the landing was served with: the address bar is left as it is until the frame moves. */
  var served = frame ? frame.getAttribute("src") : "";
  var servedMode = stage && stage.classList.contains("dp-live__stage--phone") ? "phone" : "desktop";
  var lastPage = served;
  var pendingHref = "";
  var signingOut = false;

  function landingUrl(page, mode, lang) {
    var query = "?page=" + encodeURIComponent(page).replace(/%2F/g, "/");
    if (mode && mode !== "desktop") {
      query += "&frame=" + mode;
    }
    if (lang && !prefix.test(page)) {
      query += "&lang=" + lang;
    }
    return map.landing + query;
  }

  function currentMode() {
    return stage && stage.classList.contains("dp-live__stage--phone") ? "phone" : "desktop";
  }

  /* What the strip knows of a path: [state, languages, title] — from the pages, or from the pattern
     of a page type whose address carries an id. */
  function lookup(path) {
    if (map.pages && map.pages[path]) {
      return map.pages[path];
    }
    var patterns = map.patterns || [];
    for (var index = 0; index < patterns.length; index += 1) {
      if (new RegExp(patterns[index][0]).test(path)) {
        return [patterns[index][1], "fr ar", patterns[index][2]];
      }
    }
    return null;
  }

  function follow(page, doc) {
    var path = page.split("?")[0];
    var entry = lookup(path);
    var state = entry ? entry[0] : map.fallback;
    var label = map.labels[state] || map.labels[map.fallback];
    var mode = currentMode();
    var neutral = !prefix.test(page);
    var match = prefix.exec(page);
    var docLang = doc && doc.documentElement ? String(doc.documentElement.lang || "").slice(0, 2) : "";
    var lang = match ? match[1] : docLang || "fr";
    var langs = entry ? entry[1].split(" ") : ["fr", "ar"];
    var name = (entry && entry[2]) || (doc && doc.title) || page;
    var chip = strip.querySelector("[data-dp-state]");
    if (chip) {
      chip.className = "dp-strip__state dp-strip__state--" + state;
      chip.title = label;
      var words = chip.querySelector("[data-dp-state-label]");
      if (words) {
        words.textContent = label;
        /* «V4 + fondation» is French, «V5 — council-passed» is not (accessibility r2 m6'). */
        if (state === "v5") {
          words.removeAttribute("lang");
        } else {
          words.lang = "fr";
        }
      }
    }
    /* Signed out, on the sign-in: the way in without a password, and the page «Entrer» then opens. */
    var signin = (map.signin || []).indexOf(path) !== -1;
    var hint = strip.querySelector("[data-dp-hint]");
    if (hint) {
      hint.hidden = !(signin && !map.persona);
    }
    var next = "";
    if (signin) {
      next = new URLSearchParams(page.split("?")[1] || "").get("next") || "";
      if (!follows.test(next)) {
        next = "";
      }
    }
    forEach(document.querySelectorAll("input[data-dp-next-field]"), function (field) {
      field.value = next;
    });
    frame.title = name + " — " + label;
    document.title = name + " · V5 dal vivo · Italy Legal Entry™";
    forEach(document.querySelectorAll("a[data-dp-lang]"), function (link) {
      var code = link.getAttribute("data-dp-lang");
      link.hidden = langs.indexOf(code) === -1;
      link.href = neutral ? landingUrl(page, mode, code) : landingUrl(page.replace(prefix, "/" + code + "/"), mode);
      if (code === lang) {
        link.setAttribute("aria-current", "true");
      } else {
        link.removeAttribute("aria-current");
      }
    });
    forEach(document.querySelectorAll("a[data-dp-open]"), function (link) {
      link.href = page;
    });
    forEach(document.querySelectorAll("a[data-dp-frame-mode]"), function (link) {
      link.href = landingUrl(page, link.getAttribute("data-dp-frame-mode"), neutral ? lang : "");
    });
    forEach(document.querySelectorAll("input[data-dp-page-field]"), function (field) {
      field.value = page;
    });
    forEach(document.querySelectorAll("input[data-dp-lang-field]"), function (field) {
      field.value = lang;
    });
    lastPage = page;
    if (window.history && window.history.replaceState && (page !== served || mode !== servedMode)) {
      window.history.replaceState(null, "", landingUrl(page, mode, neutral ? lang : "") + window.location.hash);
    }
  }

  function setMode(mode) {
    stage.classList.toggle("dp-live__stage--phone", mode === "phone");
    stage.classList.toggle("dp-live__stage--desktop", mode !== "phone");
    forEach(document.querySelectorAll("a[data-dp-frame-mode]"), function (link) {
      if (link.getAttribute("data-dp-frame-mode") === mode) {
        link.setAttribute("aria-current", "true");
      } else {
        link.removeAttribute("aria-current");
      }
    });
    forEach(document.querySelectorAll("input[data-dp-frame-field]"), function (field) {
      field.value = mode;
    });
  }

  /* The page the frame was asked for cannot be shown in it: the stage says so, never a blank frame. */
  function blocked(on) {
    var message = stage.querySelector("[data-dp-blocked]");
    if (!message) {
      return;
    }
    stage.classList.toggle("dp-live__stage--blocked", on);
    message.hidden = !on;
    if (!on) {
      return;
    }
    var alone = message.querySelector("[data-dp-blocked-open]");
    if (alone) {
      alone.hidden = !pendingHref;
      alone.href = pendingHref || lastPage;
    }
    var back = message.querySelector("[data-dp-blocked-back]");
    if (back) {
      back.href = landingUrl(lastPage, currentMode(), "");
    }
  }

  /* What the framed page does next: the address a link asks for (shown alone if the frame cannot hold
     it), and the product's own sign-out. */
  function watch(doc) {
    doc.addEventListener(
      "click",
      function (event) {
        var link = event.target && event.target.closest ? event.target.closest("a[href]") : null;
        if (link && !link.target) {
          pendingHref = link.href;
        }
      },
      true
    );
    doc.addEventListener(
      "submit",
      function (event) {
        var form = event.target;
        pendingHref = "";
        try {
          signingOut = /\/compte\/logout\/$/.test(new URL(form.action, doc.baseURI).pathname);
        } catch (error) {
          signingOut = false;
        }
      },
      true
    );
  }

  function framed() {
    var doc = null;
    var where = null;
    try {
      doc = frame.contentDocument;
      where = frame.contentWindow.location;
      if (!doc || !where || where.href === "about:blank" || where.origin !== window.location.origin) {
        doc = null;
      }
    } catch (error) {
      doc = null; /* another origin, or the browser's own page for a refused one */
    }
    if (!doc) {
      blocked(true);
      return;
    }
    blocked(false);
    watch(doc);
    if (signingOut && map.persona) {
      /* The session ended inside the product: the strip is served again, as the session now is. */
      window.location.replace(landingUrl(where.pathname + where.search, currentMode(), ""));
      return;
    }
    signingOut = false;
    pendingHref = "";
    if (follows.test(where.pathname)) {
      follow(where.pathname + where.search, doc);
    }
  }

  if (strip && frame && stage && map) {
    frame.addEventListener("load", framed);
    try {
      if (frame.contentDocument && frame.contentDocument.readyState === "complete") {
        if (frame.contentWindow.location.href !== "about:blank") {
          framed(); /* the frame was faster than this script */
        }
      }
    } catch (error) {
      framed();
    }
    document.addEventListener("click", function (event) {
      var link = event.target.closest ? event.target.closest("a[data-dp-frame-mode]") : null;
      if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
        return;
      }
      event.preventDefault();
      setMode(link.getAttribute("data-dp-frame-mode"));
      var menu = link.closest("details");
      if (menu) {
        menu.open = false;
        menu.querySelector("summary").focus(); /* the chip that had the focus is gone with its panel */
      }
      var query = new URLSearchParams(window.location.search);
      var page = query.get("page") || served;
      if (window.history && window.history.replaceState) {
        window.history.replaceState(
          null,
          "",
          landingUrl(page, currentMode(), query.get("lang") || "") + window.location.hash
        );
      }
    });
  }

  /* ------------------------------------------------------------------ 3 */
  var viewer = document.querySelector("dialog[data-dp-viewer]");
  if (!viewer || typeof viewer.showModal !== "function") {
    return;
  }

  /* One pair: the desktop frame and the phone frame of ONE address. */
  var MAX_FRAMES = 2;
  /* The desktop frame's own viewport, and its two hairlines. */
  var DESKTOP = { width: 1440 + 2, height: 900 + 2 };
  var holder = viewer.querySelector("[data-dp-frames]");
  var title = viewer.querySelector("[data-dp-viewer-title]");
  var alone = viewer.querySelector("[data-dp-viewer-alone]");
  var trueSize = viewer.querySelector("button[data-dp-true-size]");
  var held = { url: "", title: "", frames: [] };
  var pending = 0;
  var lastUnload = -Infinity;

  function now() {
    return window.performance && window.performance.now ? window.performance.now() : Date.now();
  }

  function kindOf(item) {
    return item.getAttribute("data-dp-kind");
  }

  /* Draw the desktop frame scaled to fit beside the phone — its page is still laid out at 1440. */
  function fit() {
    var desktop = holder.querySelector(".dp-viewer__frame--desktop");
    if (!desktop) {
      return;
    }
    var scale = 1;
    if (!trueSize || trueSize.getAttribute("aria-pressed") !== "true") {
      var style = window.getComputedStyle(holder);
      var gap = parseFloat(style.columnGap) || 0;
      var width = holder.clientWidth - (parseFloat(style.paddingLeft) || 0) - (parseFloat(style.paddingRight) || 0);
      var height = holder.clientHeight - (parseFloat(style.paddingTop) || 0) - (parseFloat(style.paddingBottom) || 0);
      var phone = holder.querySelector(".dp-viewer__frame--phone");
      if (phone) {
        width -= phone.offsetWidth + gap;
      }
      scale = Math.min(1, width / DESKTOP.width, height / DESKTOP.height);
      scale = Math.max(0.25, Math.floor(scale * 1000) / 1000);
    }
    holder.style.setProperty("--dp-scale", String(scale));
  }

  function pressed() {
    forEach(viewer.querySelectorAll("button[data-dp-add]"), function (button) {
      var kind = button.getAttribute("data-dp-add");
      var on = held.frames.some(function (item) {
        return kindOf(item) === kind;
      });
      button.setAttribute("aria-pressed", on ? "true" : "false");
    });
    /* «1:1» acts on the desktop frame: without one, there is nothing to press (accessibility r2 n2). */
    if (trueSize) {
      trueSize.disabled = !held.frames.some(function (item) {
        return kindOf(item) === "desktop";
      });
    }
  }

  /* Empty and remove the held frames — all of them, or the one of ``kind``. */
  function unload(kind) {
    var removed = false;
    held.frames = held.frames.filter(function (item) {
      if (kind && kindOf(item) !== kind) {
        return true;
      }
      removed = true;
      item.src = "about:blank";
      var box = item.parentNode && item.parentNode.classList.contains("dp-viewer__fit") ? item.parentNode : item;
      box.remove();
      return false;
    });
    if (!held.frames.length) {
      window.clearTimeout(pending);
      pending = 0;
    }
    if (!kind) {
      held.url = "";
    }
    /* Only a frame really removed starts the wait: a first open removes nothing (performance r2 P-4). */
    if (removed) {
      lastUnload = now();
    }
    pressed();
    fit();
  }

  /* Give the held frames their address: at once (the next task) when no frame was removed in the
     last 300 ms — a person's first click is not delayed — and after 150 ms otherwise; an unload
     cancels it. */
  function request() {
    window.clearTimeout(pending);
    pending = window.setTimeout(
      function () {
        pending = 0;
        held.frames.forEach(function (item) {
          if (!item.getAttribute("src")) {
            item.src = item.getAttribute("data-dp-src");
          }
        });
      },
      now() - lastUnload > 300 ? 0 : 150
    );
  }

  function load(url, kind, label) {
    if (held.url !== url) {
      unload(); /* the pair that is open goes before the next one comes */
      held.url = url;
      held.title = label;
    }
    var existing = held.frames.filter(function (item) {
      return kindOf(item) === kind;
    })[0];
    if (!existing) {
      if (held.frames.length >= MAX_FRAMES) {
        unload();
        held.url = url;
        held.title = label;
      }
      var created = document.createElement("iframe");
      created.className = "dp-viewer__frame dp-viewer__frame--" + kind;
      created.setAttribute("data-dp-kind", kind);
      created.setAttribute("data-dp-src", url);
      created.title = label + " — " + (kind === "phone" ? "Telefono 390" : "Desktop 1440");
      if (kind === "desktop") {
        var box = document.createElement("div");
        box.className = "dp-viewer__fit";
        box.appendChild(created);
        holder.insertBefore(box, holder.firstChild);
      } else {
        holder.appendChild(created);
      }
      held.frames.push(created);
      request();
    }
    title.textContent = label;
    alone.href = url;
    pressed();
    if (!viewer.open) {
      viewer.showModal();
    }
    fit();
  }

  document.addEventListener("click", function (event) {
    var link = event.target.closest ? event.target.closest("a[data-dp-pair]") : null;
    if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return;
    }
    event.preventDefault();
    load(link.getAttribute("data-dp-pair"), link.getAttribute("data-dp-kind"), link.getAttribute("data-dp-title"));
  });

  viewer.addEventListener("click", function (event) {
    var add = event.target.closest ? event.target.closest("button[data-dp-add]") : null;
    if (add && held.url) {
      var kind = add.getAttribute("data-dp-add");
      if (add.getAttribute("aria-pressed") === "true") {
        unload(kind); /* a pressed frame button releases its own frame */
      } else {
        load(held.url, kind, held.title);
      }
      return;
    }
    if (trueSize && event.target.closest && event.target.closest("button[data-dp-true-size]")) {
      trueSize.setAttribute("aria-pressed", trueSize.getAttribute("aria-pressed") === "true" ? "false" : "true");
      fit();
      return;
    }
    if (event.target.closest && event.target.closest("button[data-dp-close]")) {
      unload(); /* at once — the close event comes a task later */
      viewer.close();
    }
  });

  viewer.addEventListener("close", function () {
    unload();
  });
  window.addEventListener("resize", function () {
    if (viewer.open) {
      fit();
    }
  });
})();
