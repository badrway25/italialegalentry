/**
 * F · the measured connector «il flusso» (design V5.22, SECTION_SYSTEM_V2 §2 F; lane S). A split chunk loaded by
 * rise.js for [data-sec-js~="flow"]: inside a [data-flow] wrapper (a box around the list, never the list itself: the
 * overlay is never a list's child), one curved line through the centres of its real boxes ([data-flow-node], in
 * order) — an SVG overlay, aria-hidden, re-measured by a ResizeObserver, so a wrap, a font swap or an Arabic page (the
 * boxes stand right to left) redraws it by itself. The path's twin is the light: a dash of the same path that the end
 * call's hover and focus send along it once (v5/_sec-flusso.css; components/sezioni/flusso.html). Without script the
 * boxes stand as they are; under reduced motion the line is drawn, still.
 */
const NS = "http://www.w3.org/2000/svg";

function draw(root, svg, paths) {
  const box = root.getBoundingClientRect();
  const nodes = [...root.querySelectorAll("[data-flow-node]")].map((node) => {
    const b = node.getBoundingClientRect();
    return [b.left + b.width / 2 - box.left, b.top + b.height / 2 - box.top];
  });
  svg.setAttribute("viewBox", `0 0 ${Math.round(box.width)} ${Math.round(box.height)}`);
  let d = "";
  nodes.forEach(([x, y], i) => {
    if (!i) {
      d = `M${x} ${y}`;
      return;
    }
    const [px, py] = nodes[i - 1];
    const bend = (x - px) / 2;
    d += `C${px + bend} ${py} ${x - bend} ${y} ${x} ${y}`;
  });
  paths.forEach((path) => path.setAttribute("d", d));
}

export default function initFlow() {
  document.querySelectorAll("[data-sec-js~='flow'] [data-flow], [data-sec-js~='flow'][data-flow]").forEach((root) => {
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "flow__svg");
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("focusable", "false");
    const paths = ["flow__path", "flow__luce"].map((name) => {
      const path = document.createElementNS(NS, "path");
      path.setAttribute("class", name);
      path.setAttribute("pathLength", "1");
      svg.append(path);
      return path;
    });
    root.prepend(svg);
    const observer = new ResizeObserver(() => draw(root, svg, paths));
    observer.observe(root);
    addEventListener("pagehide", () => observer.disconnect(), { once: true });
  });
}
