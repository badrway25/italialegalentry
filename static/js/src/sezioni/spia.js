/**
 * L / I · the scroll-spy rail «la spia» (design V5.22, SECTION_SYSTEM_V2 §2 I and L, form 3; lane S). A split chunk
 * loaded by rise.js for [data-sec-js~="spia"]: a sticky index whose indicator plate glides to the part in view. The
 * current link takes aria-current="location" (announced on focus only — nothing is ever read out on scroll) and the
 * indicator its place (`--spia-y`, `--spia-h`, v5/_sec-filo.css / _sec-indice.css). No scroll listener: one
 * IntersectionObserver on the parts, disconnected when the page leaves.
 * Parts laid out as a grid (lane P2's QA_ROUND2 M3: the glossary's register, the Forum's paired sections): parts that
 * share a row cross the band together, so they are ONE stop — marked from its first (aria-current), the indicator
 * spanning their links and the others flagged `data-spia-con`; a followed link is current at once and stays so
 * through the scroll it started.
 */
export default function initSpia() {
  document.querySelectorAll("[data-sec-js~='spia']").forEach((root) => {
    const links = [...root.querySelectorAll("a[href^='#']")];
    const parts = links.map((link) => document.getElementById(decodeURIComponent(link.hash.slice(1))));
    if (!links.length || parts.includes(null)) return;
    const rail = links[0].closest("ol, ul") || root;
    let held = false;
    let timer = 0;
    const mark = (first, last = first) => {
      links.forEach((link, k) => {
        if (k === first) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
        link.toggleAttribute("data-spia-con", k > first && k <= last);
      });
      const top = rail.getBoundingClientRect().top;
      const a = links[first].getBoundingClientRect();
      rail.style.setProperty("--spia-y", `${Math.round(a.top - top)}px`);
      rail.style.setProperty("--spia-h", `${Math.round(links[last].getBoundingClientRect().bottom - a.top)}px`);
      rail.dataset.spia = "";
    };
    // the stop of a part: the parts on its row (the same top, to the pixel), in the index's order
    const stop = (i) => {
      const y = parts[i].getBoundingClientRect().top;
      const row = parts.map((part, k) => (Math.abs(part.getBoundingClientRect().top - y) < 2 ? k : -1)).filter((k) => k >= 0);
      mark(row[0], row[row.length - 1]);
    };
    const band = new Set(); // the parts crossing the band now
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => band[entry.isIntersecting ? "add" : "delete"](entry.target));
        if (held) return;
        const lit = entries.filter((entry) => entry.isIntersecting).map((entry) => parts.indexOf(entry.target));
        if (lit.length) stop(Math.max(...lit));
      },
      { rootMargin: "-35% 0px -60% 0px" },
    );
    parts.forEach((part) => observer.observe(part));
    // the last part is lit once most of it shows, though it may never cross the band (21st «Scroll Spy» 23554: «the one
    // every hand-rolled spy forgets to light») — only while no part holds the band, so it never lights ahead of a row
    // still being read
    const last = new IntersectionObserver((entries) => !held && !band.size && entries[0].isIntersecting && stop(parts.length - 1), { threshold: 0.6 });
    last.observe(parts[parts.length - 1]);
    // a followed link (a click, or Enter from the keyboard) is current at once, alone, and stays so while the scroll it
    // started runs: the parts it crosses on its way do not take the mark
    rail.addEventListener("click", (event) => {
      const i = links.indexOf(event.target.closest("a"));
      if (i < 0) return;
      mark(i);
      held = true;
      clearTimeout(timer);
      timer = setTimeout(() => (held = false), 1000);
    });
    addEventListener("pagehide", () => (observer.disconnect(), last.disconnect()), { once: true });
  });
}
