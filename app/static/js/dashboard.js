document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("diagnosisForm");
  const resultContainer = document.getElementById("diagnosis-result-container");
  const resultContent = document.getElementById("diagnosis-result-content");
  const feedback = document.getElementById("diagnosisFeedback");

  if (!form || !resultContainer || !resultContent || !feedback) {
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    feedback.classList.remove("hidden");
    feedback.textContent = "Compiling physician consultation brief...";

    const formData = new FormData(form);

    try {
      const response = await fetch(form.action || window.location.pathname, {
        method: "POST",
        body: formData,
        headers: {
          "Accept": "application/json"
        }
      });

      const payload = await response.json();
      if (payload.redirect) {
        window.location.href = payload.redirect;
        return;
      }

      if (!response.ok || !payload.success) {
        throw new Error(payload.error || "Unable to compile consultation briefing. Please try again.");
      }

      resultContainer.classList.remove("hidden");
      resultContent.innerHTML = payload.html;
      feedback.textContent = "Physician consultation brief generated successfully.";
      resultContainer.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
      feedback.textContent = error.message;
    }
  });
});
