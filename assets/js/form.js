(function () {
  var form = document.getElementById("enquiry");
  var statusBox = document.getElementById("status");
  var interestField = document.getElementById("interest-source");
  var markerEl = document.getElementById("enquiry-marker");
  var headingEl = document.getElementById("enquiry-heading");
  var introEl = document.getElementById("enquiry-intro");
  var nbsp = "\u00a0 ";
  var warning = "Please do not send customer names, passwords, confidential documents, detailed financial information or sensitive personal data.";
  var review = "I will review the enquiry personally and reply using the business email you provide.";
  var INTERESTS = {
    "focused-build": {
      marker: "Focused build",
      heading: "Tell me about the workflow you want to improve.",
      intro: "Give a general outline of the workflow, who uses it and what should work better." + nbsp + warning + nbsp + review
    },
    "workflow-diagnostic": {
      marker: "Workflow diagnostic",
      heading: "Tell me where the workflow lacks clarity.",
      intro: "A general description is enough." + nbsp + "I will help identify the smallest useful starting point." + nbsp + warning + nbsp + review
    },
    "ai-team-training": {
      marker: "AI team training",
      heading: "Tell me about the team and the work where AI could help.",
      intro: "Tell me the team's roles and the recurring work they want to approach more safely and usefully." + nbsp + warning + nbsp + review
    }
  };
  var selectedInterest = "";

  function applyInterest(key) {
    var context = INTERESTS[key];
    if (!context) return false;
    selectedInterest = key;
    if (interestField) interestField.value = key;
    if (markerEl) markerEl.textContent = context.marker;
    if (headingEl) headingEl.textContent = context.heading;
    if (introEl) introEl.textContent = context.intro;
    return true;
  }

  if (typeof URLSearchParams === "function") {
    var params = new URLSearchParams(location.search);
    var requested = params.get("interest");
    if (requested && INTERESTS[requested]) applyInterest(requested);
    if (params.has("interest") && history.replaceState) {
      history.replaceState({}, "", location.pathname + location.hash);
    }
  }

  if (!form || !statusBox) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (!form.reportValidity()) return;

    var submitted = document.getElementById("submitted-at");
    if (submitted) submitted.value = new Date().toISOString();
    if (interestField) interestField.value = selectedInterest;

    var host = location.hostname;
    var local = location.protocol === "file:" || host === "localhost" || host === "127.0.0.1";
    if (local) {
      statusBox.className = "status success";
      statusBox.innerHTML = "The form is valid.&nbsp; Enquiries are sent only from the published website.";
      statusBox.focus();
      return;
    }

    var button = form.querySelector("button");
    if (button) button.disabled = true;
    statusBox.className = "status";

    var body = new URLSearchParams(new FormData(form)).toString();
    fetch("/", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body
    }).then(function (response) {
      if (!response.ok) throw new Error("Submission failed");
      form.reset();
      if (interestField) interestField.value = selectedInterest;
      statusBox.className = "status success";
      statusBox.innerHTML = "Enquiry received.&nbsp; I will review what you have shared and respond personally.&nbsp; Please do not send confidential material unless we agree a safe method.";
    }).catch(function () {
      statusBox.className = "status error";
      statusBox.innerHTML = "The enquiry could not be sent.&nbsp; Please try again or email mat@proofsystems.co.uk.";
    }).then(function () {
      if (button) button.disabled = false;
      statusBox.focus();
    });
  });
})();
