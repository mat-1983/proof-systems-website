(function () {
  document.documentElement.classList.add("js");

  var reducedQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  var storyStaticQuery = window.matchMedia("(max-width: 900px), (max-height: 760px)");
  var nav = document.querySelector(".site-nav");
  var hero = document.querySelector("[data-hero]");
  var opening = document.querySelector("[data-v2-opening]");
  var story = document.querySelector("[data-work-story]");
  var frame = 0;

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
    var travel = Math.max(element.offsetHeight - window.innerHeight, 1);
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
    var cue = opening.querySelector(".v2-scroll-cue");
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
    cue.style.opacity = String(1 - ease(phase(0.72, 0.92, progress)));
  }

  function renderStory() {
    if (!story) return;
    var progress = reducedQuery.matches || storyStaticQuery.matches ? 1 : progressThrough(story);
    var step = progress < 0.22 ? 1 : progress < 0.48 ? 2 : progress < 0.74 ? 3 : 4;
    var thread = story.querySelector(".v2-thread-live");
    var token = story.querySelector(".v2-work-token");
    var stops = [[15, 21], [37, 45], [59, 33], [84, 75]];
    var scaled = progress * (stops.length - 1);
    var index = Math.min(stops.length - 2, Math.floor(scaled));
    var local = ease(scaled - index);
    var left = stops[index][0] + (stops[index + 1][0] - stops[index][0]) * local;
    var top = stops[index][1] + (stops[index + 1][1] - stops[index][1]) * local;

    story.setAttribute("data-story-step", String(step));
    if (thread) thread.style.strokeDashoffset = String(1 - progress);
    if (token) {
      token.style.left = left + "%";
      token.style.top = top + "%";
    }
  }

  function render() {
    frame = 0;
    renderOpening();
    renderStory();
  }

  function requestRender() {
    if (frame) return;
    frame = window.requestAnimationFrame(render);
  }

  function syncMotionMode() {
    var animate = !reducedQuery.matches;
    document.documentElement.classList.toggle("motion-ready", animate);
    document.documentElement.classList.toggle("story-static", storyStaticQuery.matches);
    if (opening) opening.setAttribute("data-opening-progress", animate ? "0" : "1");
    if (story) story.setAttribute("data-story-step", "4");
    render();
  }

  if (opening || story) {
    window.addEventListener("scroll", requestRender, { passive: true });
    window.addEventListener("resize", requestRender);
    if (typeof reducedQuery.addEventListener === "function") reducedQuery.addEventListener("change", syncMotionMode);
    if (typeof storyStaticQuery.addEventListener === "function") storyStaticQuery.addEventListener("change", syncMotionMode);
    syncMotionMode();
  }

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

  document.querySelectorAll("[data-reveal]").forEach(function (element) {
    if (reducedQuery.matches || !("IntersectionObserver" in window)) {
      element.classList.add("is-visible");
      return;
    }
    new IntersectionObserver(function (entries, observer) {
      if (!entries[0].isIntersecting) return;
      element.classList.add("is-visible");
      observer.disconnect();
    }, { threshold: 0.12 }).observe(element);
  });

  function loadTeaser(element) {
    var src = element.getAttribute("data-teaser-src");
    if (!src || element.querySelector("video")) return;
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
