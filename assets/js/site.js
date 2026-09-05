(function () {
  document.documentElement.classList.add("js");

  var reducedQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  var nav = document.querySelector(".site-nav");
  var hero = document.querySelector("[data-hero]");
  var opening = document.querySelector("[data-v2-opening]");
  var story = document.querySelector("[data-work-story]");
  var tracks = Array.prototype.slice.call(document.querySelectorAll("[data-scroll-track]"));
  var frame = 0;
  var needsMeasure = true;
  // Small viewport units keep narrative travel stable as mobile browser chrome moves.
  var viewportProbe = document.createElement("div");
  viewportProbe.style.cssText = "position:fixed;height:100svh;width:0;visibility:hidden;pointer-events:none";
  viewportProbe.setAttribute("aria-hidden", "true");
  document.body.appendChild(viewportProbe);

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function phase(start, end, value) {
    return clamp((value - start) / (end - start), 0, 1);
  }

  function ease(value) {
    return value * value * (3 - (2 * value));
  }

  function progressThrough(element) {
    var rect = element.getBoundingClientRect();
    var sticky = element.querySelector(".v2-opening-sticky");
    var travel = Math.max(element.offsetHeight - (sticky ? sticky.offsetHeight : window.innerHeight), 1);
    return clamp(-rect.top / travel, 0, 1);
  }

  function setPath(path, points) {
    if (!path) return;
    function point(index) {
      return points[index][0].toFixed(2) + " " + points[index][1].toFixed(2);
    }
    if (path.classList.contains("v2-mark-main")) {
      path.setAttribute("d", "M" + point(0) + " L" + point(1) + " L" + point(2));
    } else if (path.classList.contains("v2-mark-branch-one")) {
      path.setAttribute("d", "M" + point(3) + " L" + point(1));
    } else {
      path.setAttribute("d", "M" + point(4) + " L" + point(1));
    }
  }

  function renderOpening() {
    if (!opening) return;
    var mark = opening.querySelector(".v2-opening-mark-wrap");
    var svg = opening.querySelector(".v2-opening-mark");
    var outline = opening.querySelector(".v2-mark-outline");
    var main = opening.querySelector(".v2-mark-main");
    var branches = opening.querySelectorAll(".v2-mark-branch");
    var nodes = opening.querySelectorAll(".v2-mark-node");
    var name = opening.querySelector(".v2-opening-name");
    var lines = opening.querySelectorAll(".v2-opening-copy h1 span");
    var progress = reducedQuery.matches ? 1 : progressThrough(opening);
    var settle = ease(phase(0, 0.36, progress));
    var depth = 1 - settle;
    var assemble = ease(phase(0.03, 0.40, progress));
    var lift = ease(phase(0.31, 0.60, progress));
    var offsets = [[-16, 7], [0, 16], [17, -8], [-8, -15], [13, 14]];
    var originals = [[108, 200], [168, 268], [304, 132], [148, 132], [252, 228]];
    var points = originals.map(function (point, index) {
      return [point[0] + offsets[index][0] * depth, point[1] + offsets[index][1] * depth];
    });

    opening.setAttribute("data-opening-progress", progress.toFixed(3));
    mark.style.transform = "translateY(" + (-2.2 * lift) + "vh) scale(" + (1 - 0.08 * lift) + ")";
    svg.style.transform = "perspective(850px) rotateX(" + (depth * 9) + "deg) rotateY(" + (-depth * 7) + "deg)";
    main.style.strokeDashoffset = String(1 - assemble);
    branches.forEach(function (branch, index) {
      branch.style.strokeDashoffset = String(1 - ease(phase(0.02 + index * 0.02, 0.30 + index * 0.02, progress)));
    });
    outline.style.strokeDashoffset = String(1 - ease(phase(0.15, 0.44, progress)));
    outline.style.opacity = String(0.25 + 0.75 * settle);
    setPath(main, points);
    setPath(branches[0], points);
    setPath(branches[1], points);
    nodes.forEach(function (node, index) {
      var offset = offsets[index];
      node.style.transform = "translate(" + (offset[0] * depth) + "px," + (offset[1] * depth) + "px) scale(" + (1 + depth * (index === 1 ? 0.055 : -0.025)) + ")";
      node.style.filter = index > 2 ? "blur(" + (depth * 0.5) + "px)" : "none";
    });

    var nameReveal = ease(phase(0.40, 0.59, progress));
    name.style.opacity = String(nameReveal);
    name.style.transform = "translateY(" + ((1 - nameReveal) * 34) + "px)";
    lines.forEach(function (line, index) {
      var reveal = ease(phase(0.52 + index * 0.075, 0.68 + index * 0.075, progress));
      line.style.opacity = String(reveal);
      line.style.transform = "translateY(" + ((1 - reveal) * 28) + "px)";
    });
  }

  function measureTracks() {
    needsMeasure = false;
    var navHeight = nav ? nav.offsetHeight : 0;
    var stableHeight = viewportProbe.offsetHeight || window.innerHeight;
    tracks.forEach(function (track) {
      var stage = track.querySelector(".scroll-stage");
      var panels = track.querySelectorAll("[data-stage-panel]");
      var tallest = 0;
      panels.forEach(function (panel) { tallest = Math.max(tallest, panel.offsetHeight); });
      track.style.setProperty("--panels-height", tallest + "px");
      var inner = stage.querySelector(".wrap");
      var styles = getComputedStyle(stage);
      var naturalHeight = inner.offsetHeight + parseFloat(styles.paddingTop) + parseFloat(styles.paddingBottom);
      var stageHeight = Math.max(160, stableHeight - navHeight);
      if (panels.length) {
        // Reserve space for the persistent indicator and disclosure. Oversized cards
        // read from top to bottom during their native-scroll hold, without a nested scroller.
        var panelSpace = Math.max(80, stageHeight - (naturalHeight - tallest));
        track.style.setProperty("--panels-height", Math.min(tallest, panelSpace) + "px");
      }
      track.style.setProperty("--stage-height", stageHeight + "px");
      track.style.setProperty("--stage-top", navHeight + "px");
      track.style.setProperty("--scroll-travel", Math.max(600, stableHeight * (panels.length ? 4.5 : 2.5), panels.length ? tallest * 5 : naturalHeight * 2.5) + "px");
      track.setAttribute("data-overflow", naturalHeight > stageHeight ? "true" : "false");
      if (track.dataset.scrollTrack === "connection") measureWires(track);
    });
  }

  function measureWires(track) {
    var board = track.querySelector(".connection-board");
    var boardRect = board.getBoundingClientRect();
    function box(selector) {
      var rect = board.querySelector(selector).getBoundingClientRect();
      return { x: rect.left - boardRect.left, y: rect.top - boardRect.top, w: rect.width, h: rect.height };
    }
    var left = box(".connection-source:first-child");
    var right = box(".connection-source:last-child");
    var layer = box(".connection-layer");
    var outcome = box(".connection-outcome");
    // Use layout offsets: the layer's scroll transform must not change its route endpoint.
    var layerElement = board.querySelector(".connection-layer");
    layer.x = layerElement.offsetLeft; layer.y = layerElement.offsetTop;
    var outcomeElement = board.querySelector(".connection-outcome");
    outcome.x = outcomeElement.offsetLeft; outcome.y = outcomeElement.offsetTop;
    var horizontal = left.x + left.w < layer.x;
    function path(from, to) {
      var x1 = horizontal ? from.x + from.w : from.x + from.w / 2;
      var y1 = horizontal ? from.y + from.h / 2 : from.y + from.h;
      var x2 = horizontal ? to.x : to.x + to.w / 2;
      var y2 = horizontal ? to.y + to.h / 2 : to.y;
      return horizontal ? "M" + x1 + " " + y1 + " C" + ((x1+x2)/2) + " " + y1 + " " + ((x1+x2)/2) + " " + y2 + " " + x2 + " " + y2 :
        "M" + x1 + " " + y1 + " C" + x1 + " " + ((y1+y2)/2) + " " + x2 + " " + ((y1+y2)/2) + " " + x2 + " " + y2;
    }
    board.querySelector('[data-wire="left"]').setAttribute("d", path(left, layer));
    board.querySelector('[data-wire="right"]').setAttribute("d", path(right, layer));
    board.querySelector('[data-wire="out"]').setAttribute("d", path(layer, outcome));
  }

  function trackProgress(track) {
    var stage = track.querySelector(".scroll-stage");
    var travel = Math.max(track.offsetHeight - stage.offsetHeight, 1);
    var top = parseFloat(getComputedStyle(stage).top) || 0;
    return clamp((top - track.getBoundingClientRect().top) / travel, 0, 1);
  }

  function renderTracks() {
    tracks.forEach(function (track) {
      var progress = reducedQuery.matches ? 1 : trackProgress(track);
      track.setAttribute("data-progress", progress.toFixed(4));
      var panels = track.querySelectorAll("[data-stage-panel]");
      var selected = Math.min(3, Math.floor(progress * 4));
      track.setAttribute("data-active-stage", String(selected + 1));
      if (track.dataset.scrollTrack === "story" && story) story.setAttribute("data-story-step", String(selected + 1));
      panels.forEach(function (panel, index) {
        var position = progress * 4 - index;
        var enter = index === 0 ? 1 : ease(phase(-0.12, 0.12, position));
        var leave = index === panels.length - 1 ? 0 : ease(phase(0.88, 1.12, position));
        var opacity = enter * (1 - leave);
        var distance = track.dataset.scrollTrack === "process" ? 110 : 38;
        panel.style.opacity = String(opacity);
        var overflow = Math.max(0, panel.offsetHeight - panel.parentElement.offsetHeight);
        var readTravel = overflow * ease(phase(0.20, 0.70, position));
        panel.style.transform = "translateY(" + ((1-enter-leave) * distance - readTravel) + "px)";
        panel.classList.toggle("is-current", opacity > 0.001);
        // These panels contain narrative only; hidden content cannot create invisible focus stops.
      });
      track.querySelectorAll("[data-stage-indicator]").forEach(function (item, index) {
        item.classList.toggle("is-current", index === selected);
      });
      var thread = track.querySelector(".story-thread i");
      if (thread) thread.style.transform = "scaleX(" + progress + ")";
      var light = track.querySelector(".process-light");
      if (light) light.style.transform = "translate(" + (25 - progress*50) + "%," + (-10 + progress*20) + "%)";
      if (track.dataset.scrollTrack === "connection") {
        var board = track.querySelector(".connection-board");
        var stage = track.querySelector(".scroll-stage");
        var stageStyles = getComputedStyle(stage);
        var boardOverflow = Math.max(0, board.offsetHeight + parseFloat(stageStyles.paddingTop) + parseFloat(stageStyles.paddingBottom) - stage.offsetHeight);
        board.style.transform = "translateY(" + (-boardOverflow * ease(phase(0.16, 0.90, progress))) + "px)";
        var flow = ease(phase(0.08, 0.57, progress));
        track.querySelectorAll(".connection-wire").forEach(function (wire) {
          var amount = wire.dataset.wire === "out" ? ease(phase(0.63, 0.83, progress)) : flow;
          wire.style.strokeDashoffset = String(1 - amount);
          wire.style.opacity = amount > 0 ? "1" : "0";
        });
        var arrive = ease(phase(0.43, 0.66, progress));
        var finish = ease(phase(0.74, 0.93, progress));
        var layer = track.querySelector(".connection-layer");
        var outcome = track.querySelector(".connection-outcome");
        layer.style.opacity = String(arrive);
        layer.style.transform = "translateY(" + ((1-arrive)*24) + "px)";
        outcome.style.opacity = String(finish);
        outcome.style.transform = "translateY(" + ((1-finish)*15) + "px)";
        track.querySelector(".connection-caption").textContent = progress < 0.38 ? "The work finds a way around the software." : progress < 0.78 ? "Connect the gaps around the systems you have." : "The software follows the work.";
      }
    });
  }

  function render() {
    frame = 0;
    if (needsMeasure) measureTracks();
    renderOpening();
    renderTracks();
  }

  function requestRender() {
    if (frame) return;
    frame = window.requestAnimationFrame(render);
  }

  function requestMeasure() { needsMeasure = true; requestRender(); }

  function syncMotionMode() {
    document.documentElement.classList.toggle("motion-ready", !reducedQuery.matches);
    if (reducedQuery.matches) {
      document.documentElement.classList.remove("reveal-ready");
      document.querySelectorAll("[data-teaser-src] video").forEach(function (video) {
        video.pause();
        video.hidden = true;
      });
    }
    needsMeasure = true;
    render();
  }

  window.addEventListener("scroll", requestRender, { passive: true });
  window.addEventListener("resize", requestMeasure);
  if (window.visualViewport) window.visualViewport.addEventListener("resize", requestMeasure);
  if (typeof reducedQuery.addEventListener === "function") reducedQuery.addEventListener("change", syncMotionMode);
  syncMotionMode();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(requestMeasure);

  if (nav && hero && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      nav.classList.toggle("is-compact", !entries[0].isIntersecting);
    }, { threshold: 0.08 }).observe(hero);
  } else if (nav && !hero) {
    nav.classList.add("is-compact");
  }

  var navOpen = document.getElementById("nav-open");
  var navToggle = document.querySelector(".nav-toggle");
  if (navOpen && navToggle) {
    function syncNav() {
      navToggle.setAttribute("aria-expanded", navOpen.checked ? "true" : "false");
    }
    navOpen.addEventListener("change", syncNav);
    document.querySelectorAll(".nav-links a").forEach(function (link) {
      link.addEventListener("click", function () {
        navOpen.checked = false;
        syncNav();
      });
    });
    syncNav();
  }

  if (!reducedQuery.matches && "IntersectionObserver" in window) document.documentElement.classList.add("reveal-ready");
  document.querySelectorAll("[data-reveal]").forEach(function (element) {
    if (reducedQuery.matches || !("IntersectionObserver" in window)) {
      element.classList.add("is-visible");
      return;
    }
    new IntersectionObserver(function (entries, observer) {
      if (!entries[0].isIntersecting) return;
      element.classList.add("is-visible");
      observer.disconnect();
    }, { threshold: 0.01 }).observe(element);
  });

  function loadTeaser(element) {
    var src = element.getAttribute("data-teaser-src");
    if (reducedQuery.matches || !src || element.querySelector("video")) return;
    var video = document.createElement("video");
    var source = document.createElement("source");
    video.muted = true;
    video.loop = true;
    video.playsInline = true;
    video.preload = "metadata";
    video.setAttribute("playsinline", "");
    video.setAttribute("aria-hidden", "true");
    video.tabIndex = -1;
    video.poster = element.getAttribute("data-poster") || "";
    source.src = src;
    source.type = "video/mp4";
    video.appendChild(source);
    element.appendChild(video);
    video.addEventListener("canplay", function () {
      if (reducedQuery.matches) return;
      var result = video.play();
      if (result && typeof result.catch === "function") result.catch(function () {});
    }, { once: true });
    video.load();
  }

  if (!reducedQuery.matches) {
    var teasers = document.querySelectorAll("[data-teaser-src]");
    if (teasers.length && "IntersectionObserver" in window) {
      var teaserObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          loadTeaser(entry.target);
          teaserObserver.unobserve(entry.target);
        });
      }, { rootMargin: "100px 0px" });
      teasers.forEach(function (element) { teaserObserver.observe(element); });
    }
  }

  function syncWorkView() {
    var connected = document.getElementById("view-connected");
    var individual = document.getElementById("view-individual");
    if (!connected || !individual) return;
    if (location.hash === "#connected-workflow" || location.hash === "#connect") connected.checked = true;
    else if (location.hash === "#finance" || location.hash === "#individual-systems") individual.checked = true;
  }

  syncWorkView();
  window.addEventListener("hashchange", syncWorkView);
  window.addEventListener("popstate", syncWorkView);
  window.addEventListener("pageshow", syncWorkView);

  var connectedInput = document.getElementById("view-connected");
  var individualInput = document.getElementById("view-individual");
  if (connectedInput && individualInput && window.history && history.pushState) {
    connectedInput.addEventListener("change", function () {
      if (connectedInput.checked && location.hash !== "#connected-workflow") {
        history.pushState({}, "", "#connected-workflow");
      }
    });
    individualInput.addEventListener("change", function () {
      if (!individualInput.checked || location.hash === "#finance") return;
      if (["#connected-workflow", "#connect", "#individual-systems"].indexOf(location.hash) !== -1) {
        history.pushState({}, "", location.pathname + location.search);
      }
    });
  }
})();
