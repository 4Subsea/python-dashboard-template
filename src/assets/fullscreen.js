// Fullscreen toggle for chart visuals. See the "Fullscreen Toggle Pattern"
// section in CLAUDE.md for the required markup and the reasoning behind
// this approach.
//
// Event delegation (rather than per-chart wiring) so this survives
// dcc.Loading re-rendering the DOM, and applies automatically to any
// current or future chart that follows the markup pattern.

function resizeGraphsIn(container) {
  if (!window.Plotly) return;
  container.querySelectorAll(".graph-wrap").forEach(function (wrap) {
    const gd = wrap.querySelector(".js-plotly-plot");
    if (!gd) return;
    const rect = wrap.getBoundingClientRect();
    const width = Math.round(rect.width);
    const height = Math.round(rect.height);
    if (width > 0 && height > 0) {
      window.Plotly.relayout(gd, { width: width, height: height, autosize: false });
    }
  });
}

function settleResize(visual) {
  requestAnimationFrame(function () {
    resizeGraphsIn(visual);
    setTimeout(function () { resizeGraphsIn(visual); }, 100);
  });
}

function exitFullscreen(visual) {
  visual.classList.remove("visual--fullscreen");
  document.body.classList.remove("fullscreen-active");
  settleResize(visual);
}

function enterFullscreen(visual) {
  document.querySelectorAll(".visual--fullscreen").forEach(function (el) {
    el.classList.remove("visual--fullscreen");
  });
  visual.classList.add("visual--fullscreen");
  document.body.classList.add("fullscreen-active");
  settleResize(visual);
}

document.addEventListener("click", function (event) {
  const btn = event.target.closest(".fullscreen-toggle-btn");
  if (!btn) return;
  const visual = btn.closest(".visual");
  if (!visual) return;
  if (visual.classList.contains("visual--fullscreen")) {
    exitFullscreen(visual);
  } else {
    enterFullscreen(visual);
  }
});

document.addEventListener("keydown", function (event) {
  if (event.key !== "Escape") return;
  const visual = document.querySelector(".visual--fullscreen");
  if (visual) exitFullscreen(visual);
});
