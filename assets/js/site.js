(function () {
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var nav = document.querySelector(".site-nav");
  var hero = document.querySelector("[data-hero]");

  if (nav && hero && "IntersectionObserver" in window) {
    var navObserver = new IntersectionObserver(function (entries) {
      nav.classList.toggle("is-compact", !entries[0].isIntersecting);
    }, { threshold: 0.12 });
    navObserver.observe(hero);
  } else if (nav && !hero) {
    nav.classList.add("is-compact");
  }

  var scenes = document.querySelectorAll("[data-workflow]");
  if (scenes.length) {
    if (reduced) {
      scenes.forEach(function (scene) { scene.style.setProperty("--progress", "1"); });
    } else {
      scenes.forEach(function (scene) { scene.style.setProperty("--progress", "0"); });
      var updateProgress = function () {
        var vh = window.innerHeight || 1;
        scenes.forEach(function (scene) {
          var rect = scene.getBoundingClientRect();
          var start = vh * 0.75;
          var end = vh * 0.2 - rect.height * 0.35;
          var raw = (start - rect.top) / (start - end || 1);
          var value = raw < 0 ? 0 : raw > 1 ? 1 : raw;
          scene.style.setProperty("--progress", String(value));
        });
      };
      updateProgress();
      window.addEventListener("scroll", updateProgress, { passive: true });
      window.addEventListener("resize", updateProgress, { passive: true });
    }
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
})();
