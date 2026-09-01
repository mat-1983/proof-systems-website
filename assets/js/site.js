(function () {
  document.documentElement.classList.add("js");
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var nav = document.querySelector(".site-nav");
  var hero = document.querySelector("[data-hero]");
  var opening = document.querySelector("[data-opening]");

  if (nav && hero && "IntersectionObserver" in window) {
    var navObserver = new IntersectionObserver(function (entries) {
      nav.classList.toggle("is-compact", !entries[0].isIntersecting);
    }, { threshold: 0.12 });
    navObserver.observe(hero);
  } else if (nav && !hero) {
    nav.classList.add("is-compact");
  }

  function clamp(n, a, b) {
    return Math.max(a, Math.min(b, n));
  }

  function updateOpening() {
    if (!opening) return;
    if (reduced) {
      opening.style.setProperty("--opening", "1");
      opening.setAttribute("data-phase", "tagline");
      return;
    }
    var rect = opening.getBoundingClientRect();
    var travel = Math.max(opening.offsetHeight - window.innerHeight * 0.55, 1);
    var progress = clamp(-rect.top / travel, 0, 1);
    opening.style.setProperty("--opening", progress.toFixed(3));
    var phase = "mark";
    if (progress >= 0.72) phase = "tagline";
    else if (progress >= 0.45) phase = "name";
    else if (progress >= 0.18) phase = "connect";
    opening.setAttribute("data-phase", phase);
  }

  if (opening) {
    if (!reduced) {
      window.addEventListener("scroll", updateOpening, { passive: true });
      window.addEventListener("resize", updateOpening);
    }
    updateOpening();
  }

  var narrowMq = window.matchMedia("(max-width: 900px)");
  function isNarrow() {
    return narrowMq.matches;
  }
  function onNarrowChange(handler) {
    if (typeof narrowMq.addEventListener === "function") {
      narrowMq.addEventListener("change", handler);
    } else if (typeof narrowMq.addListener === "function") {
      narrowMq.addListener(handler);
    }
  }

  function bindStickyScene(root, attr, steps, onStep) {
    if (!root) return;
    function update() {
      if (reduced) {
        root.setAttribute(attr, String(steps));
        if (onStep) onStep(steps);
        return;
      }
      if (root.hasAttribute("data-fluid-narrow") && isNarrow()) {
        root.setAttribute(attr, String(steps));
        if (onStep) onStep(steps);
        return;
      }
      var rect = root.getBoundingClientRect();
      var travel = Math.max(root.offsetHeight - window.innerHeight, 1);
      var progress = clamp(-rect.top / travel, 0, 1);
      var step = Math.min(steps, 1 + Math.floor(progress * steps));
      if (attr === "data-approach-step") {
        step = progress >= 0.90 ? steps : Math.min(steps - 1, 1 + Math.floor((progress / 0.90) * (steps - 1)));
      }
      if (attr === "data-fit-step" && isNarrow()) {
        if (progress < 0.12) step = 1;
        else step = Math.min(steps, 2 + Math.floor(((progress - 0.12) / 0.66) * (steps - 1)));
      }
      root.setAttribute(attr, String(step));
      if (onStep) onStep(step);
    }
    if (!reduced) {
      window.addEventListener("scroll", update, { passive: true });
      window.addEventListener("resize", update);
      onNarrowChange(update);
    }
    update();
  }

  function bindFluidJourney(root) {
    if (!root) return;
    var items = root.querySelectorAll(
      ".gap-node, .gap-callout, .gap-legend span, .approach-stage, .approach-connector, .approach-routes, .cap-leg, .cap-rail-link, .cap-rail-tail"
    );
    var observer = null;

    function reveal(el) {
      if (el.classList.contains("is-arrived")) return;
      el.classList.add("is-arrived");
      if (root.id === "gap") {
        var nodeMatch = /gap-node-(\d)/.exec(el.className);
        if (nodeMatch) {
          var index = parseInt(nodeMatch[1], 10);
          if (index >= 2) {
            var connector = root.querySelector(".gap-c" + (index - 1));
            var pulse = root.querySelector(".gap-p" + (index - 1));
            if (connector) connector.classList.add("is-arrived");
            if (pulse) pulse.classList.add("is-arrived");
          }
        }
      }
      if (root.id === "approach" && el.classList.contains("approach-stage")) {
        var approachFrom = el.getAttribute("data-approach-from");
        var incoming = root.querySelector('.approach-connector[data-approach-from="' + approachFrom + '"]');
        if (incoming) incoming.classList.add("is-arrived");
      }
      if (root.id === "approach" && el.classList.contains("approach-routes")) {
        var finalLink = root.querySelector(".approach-connector[data-approach-from='5']");
        if (finalLink) finalLink.classList.add("is-arrived");
      }
      if (root.id === "capability" && el.classList.contains("cap-leg")) {
        var capFrom = el.getAttribute("data-cap-from");
        var rail = root.querySelector('.cap-rail-link[data-cap-from="' + capFrom + '"]');
        if (rail) rail.classList.add("is-arrived");
      }
    }

    function revealAll() {
      items.forEach(reveal);
    }

    function stop() {
      if (!observer) return;
      observer.disconnect();
      observer = null;
    }

    if (reduced || !("IntersectionObserver" in window)) {
      revealAll();
      return;
    }

    function apply() {
      stop();
      if (!isNarrow()) return;
      observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          reveal(entry.target);
          if (observer) observer.unobserve(entry.target);
        });
      }, { threshold: 0.22, rootMargin: "0px 0px -8% 0px" });
      items.forEach(function (el) {
        if (el.classList.contains("is-arrived")) return;
        observer.observe(el);
      });
    }

    apply();
    onNarrowChange(apply);
  }

  var capability = document.querySelector("[data-capability]");

  function syncCapabilityActions(step) {
    var actions = capability.querySelector(".capability-actions");
    if (!actions) return;
    var expose = reduced || isNarrow() || String(step) === "6";
    if (expose) {
      actions.removeAttribute("inert");
      actions.removeAttribute("aria-hidden");
    } else {
      actions.setAttribute("inert", "");
      actions.setAttribute("aria-hidden", "true");
    }
  }

  bindStickyScene(capability, "data-cap-step", 6, function (step) {
    if (capability) syncCapabilityActions(step);
  });

  document.querySelectorAll("[data-scene]").forEach(function (scene) {
    var steps = parseInt(scene.getAttribute("data-scene-steps") || "4", 10);
    var name = scene.getAttribute("data-scene");
    bindStickyScene(scene, "data-" + name + "-step", steps);
  });

  document.querySelectorAll("[data-fluid-narrow]").forEach(bindFluidJourney);

  var scenes = document.querySelectorAll("[data-reveal]");
  if (scenes.length && !reduced && "IntersectionObserver" in window) {
    var reveal = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          reveal.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });
    scenes.forEach(function (scene) { reveal.observe(scene); });
  } else {
    scenes.forEach(function (scene) { scene.classList.add("is-visible"); });
  }

  function loadTeaser(el) {
    var src = el.getAttribute("data-teaser-src");
    if (!src || el.querySelector("video")) return;
    var video = document.createElement("video");
    video.muted = true;
    video.loop = true;
    video.playsInline = true;
    video.setAttribute("playsinline", "");
    video.preload = "metadata";
    video.setAttribute("aria-hidden", "true");
    video.tabIndex = -1;
    var poster = el.getAttribute("data-poster");
    if (poster) video.poster = poster;
    var source = document.createElement("source");
    source.src = src;
    source.type = "video/mp4";
    video.appendChild(source);
    el.appendChild(video);
    video.addEventListener("canplay", function () {
      var play = video.play();
      if (play && typeof play.catch === "function") play.catch(function () {});
    }, { once: true });
    video.load();
  }

  if (!reduced) {
    var teasers = document.querySelectorAll("[data-teaser-src]");
    if (teasers.length && "IntersectionObserver" in window) {
      var teaserObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            loadTeaser(entry.target);
            teaserObserver.unobserve(entry.target);
          }
        });
      }, { rootMargin: "100px 0px" });
      teasers.forEach(function (el) { teaserObserver.observe(el); });
    }
  }

  var navOpen = document.getElementById("nav-open");
  var toggle = document.querySelector(".nav-toggle");
  if (navOpen && toggle) {
    var sync = function () {
      toggle.setAttribute("aria-expanded", navOpen.checked ? "true" : "false");
    };
    navOpen.addEventListener("change", sync);
    sync();
  }

  function syncWorkView() {
    var connected = document.getElementById("view-connected");
    var individual = document.getElementById("view-individual");
    if (!connected || !individual) return;
    var hash = location.hash;
    if (hash === "#connected-workflow" || hash === "#connect") {
      connected.checked = true;
    } else if (hash === "#finance" || hash === "#individual-systems") {
      individual.checked = true;
    }
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
      if (!individualInput.checked) return;
      if (location.hash === "#finance") return;
      if (location.hash === "#connected-workflow" || location.hash === "#connect" || location.hash === "#individual-systems") {
        history.pushState({}, "", location.pathname + location.search);
      }
    });
  }

  var scrollCue = document.querySelector(".scroll-cue");
  function updateScrollCue() {
    if (!scrollCue) return;
    var start = document.getElementById("start");
    var remaining = document.documentElement.scrollHeight - window.innerHeight - window.scrollY;
    var startNear = start && start.getBoundingClientRect().top < window.innerHeight - 72;
    scrollCue.hidden = remaining < 48 || Boolean(startNear);
  }
  if (scrollCue) {
    window.addEventListener("scroll", updateScrollCue, { passive: true });
    window.addEventListener("resize", updateScrollCue);
    updateScrollCue();
    scrollCue.addEventListener("click", function () {
      var distance = Math.max(window.innerHeight * 0.78, 280);
      if (reduced) window.scrollBy(0, distance);
      else window.scrollBy({ top: distance, left: 0, behavior: "smooth" });
    });
  }
})();
