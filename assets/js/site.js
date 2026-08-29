(function () {
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
    if (reduced || window.matchMedia("(max-width: 760px)").matches) {
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

  var scenes = document.querySelectorAll("[data-reveal]");
  if (scenes.length && !reduced && "IntersectionObserver" in window) {
    var reveal = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) entry.target.classList.add("is-visible");
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

  var connectedInput = document.getElementById("view-connected");
  var individualInput = document.getElementById("view-individual");
  if (connectedInput && individualInput && window.history && history.replaceState) {
    connectedInput.addEventListener("change", function () {
      if (connectedInput.checked) history.replaceState({}, "", "#connected-workflow");
    });
    individualInput.addEventListener("change", function () {
      if (individualInput.checked) history.replaceState({}, "", location.pathname);
    });
  }
})();
