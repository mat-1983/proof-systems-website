(function () {
  var form = document.getElementById("enquiry");
  var statusBox = document.getElementById("status");
  if (!form || !statusBox) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (!form.reportValidity()) return;

    var submitted = document.getElementById("submitted-at");
    if (submitted) submitted.value = new Date().toISOString();

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
