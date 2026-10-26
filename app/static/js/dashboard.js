document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("diagnosisForm");
  const resultContainer = document.getElementById("diagnosis-result-container");
  const resultContent = document.getElementById("diagnosis-result-content");
  const feedback = document.getElementById("diagnosisFeedback");
  const submitBtn = document.getElementById("prepare-summary-btn");
  const originalBtnHtml = submitBtn ? submitBtn.innerHTML : "";

  if (!form || !resultContainer || !resultContent || !feedback) {
    return;
  }

  const progressTrack = document.getElementById("intakeProgressTrack");
  const heroWrapper = document.getElementById("heroSearchWrapper");

  const spinnerSvg = `
    <svg class="spinner-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <line x1="12" y1="2" x2="12" y2="6"></line>
      <line x1="12" y1="18" x2="12" y2="22"></line>
      <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line>
      <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line>
      <line x1="2" y1="12" x2="6" y2="12"></line>
      <line x1="18" y1="12" x2="22" y2="12"></line>
      <line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line>
      <line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line>
    </svg>
  `;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const symptomsVal = (document.getElementById("symptoms")?.value || "").trim();
    if (!symptomsVal) {
      if (feedback) {
        feedback.classList.remove("hidden");
        feedback.textContent = "Please enter your symptoms to receive clinical guidance.";
      }
      return;
    }

    feedback.classList.remove("hidden");
    feedback.textContent = "Analyzing clinical signs against medical guidelines...";

    if (progressTrack) progressTrack.classList.add("active");
    if (heroWrapper) heroWrapper.classList.add("is-loading");

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.classList.add("is-loading");
      submitBtn.innerHTML = `${spinnerSvg}<span>Analyzing Clinical Signs...</span>`;
    }

    const stages = [
      { btn: "Analyzing Clinical Signs...", text: "Reviewing symptom observations against clinical guidelines..." },
      { btn: "Matching 500+ Conditions...", text: "Cross-referencing symptom clusters in clinical database..." },
      { btn: "Compiling Clinical Guidance...", text: "Synthesizing personalized observations and precautions..." }
    ];

    let stageIdx = 0;
    const stageTimer = setInterval(() => {
      stageIdx++;
      if (stageIdx < stages.length) {
        if (submitBtn) {
          submitBtn.innerHTML = `${spinnerSvg}<span>${stages[stageIdx].btn}</span>`;
        }
        if (feedback) {
          feedback.textContent = stages[stageIdx].text;
        }
      }
    }, 850);

    const formData = new FormData(form);
    const submitUrl = form.getAttribute("action") || "/dashboard";

    let redirected = false;

    try {
      const response = await fetch(submitUrl, {
        method: "POST",
        body: formData,
        headers: {
          "Accept": "application/json"
        }
      });

      clearInterval(stageTimer);

      const payload = await response.json();
      if (payload.redirect) {
        redirected = true;
        if (submitBtn) {
          submitBtn.innerHTML = `
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>
            <span>Pattern Matched • Loading Questions...</span>
          `;
        }
        if (feedback) {
          feedback.textContent = "Clinical pattern matched. Loading personalized follow-up assessment...";
        }
        setTimeout(() => {
          window.location.href = payload.redirect;
        }, 180);
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
      clearInterval(stageTimer);
      feedback.textContent = error.message;
    } finally {
      clearInterval(stageTimer);
      if (!redirected) {
        if (progressTrack) progressTrack.classList.remove("active");
        if (heroWrapper) heroWrapper.classList.remove("is-loading");
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.classList.remove("is-loading");
          submitBtn.innerHTML = originalBtnHtml;
        }
      }
    }
  });

  // 2. All Health Concerns Modal Management (More and View All Buttons)
  const moreBtn = document.getElementById("moreConcernsBtn");
  const viewAllBtn = document.getElementById("viewAllConcernsBtn");
  const modalBackdrop = document.getElementById("concernsModalBackdrop");
  const modalCloseBtn = document.getElementById("closeConcernsModalBtn");
  const searchInput = document.getElementById("concernSearchInput");
  const modalItems = document.querySelectorAll(".modal-concern-item");
  const symptomsInput = document.getElementById("symptoms");

  const openConcernsModal = () => {
    if (!modalBackdrop) return;
    modalBackdrop.hidden = false;
    modalBackdrop.classList.add("is-open");
    document.body.style.overflow = "hidden";
    if (searchInput) {
      searchInput.value = "";
      filterConcerns("");
      setTimeout(() => searchInput.focus(), 150);
    }
  };

  const closeConcernsModal = () => {
    if (!modalBackdrop) return;
    modalBackdrop.classList.remove("is-open");
    setTimeout(() => {
      modalBackdrop.hidden = true;
    }, 200);
    document.body.style.overflow = "";
  };

  const filterConcerns = (query) => {
    const q = query.trim().toLowerCase();
    modalItems.forEach((item) => {
      const text = item.textContent.toLowerCase();
      const sym = (item.dataset.symptom || "").toLowerCase();
      if (!q || text.includes(q) || sym.includes(q)) {
        item.style.display = "flex";
      } else {
        item.style.display = "none";
      }
    });
  };

  if (moreBtn) {
    moreBtn.addEventListener("click", (e) => {
      e.preventDefault();
      openConcernsModal();
    });
  }

  if (viewAllBtn) {
    viewAllBtn.addEventListener("click", (e) => {
      e.preventDefault();
      openConcernsModal();
    });
  }

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener("click", closeConcernsModal);
  }

  if (modalBackdrop) {
    modalBackdrop.addEventListener("click", (e) => {
      if (e.target === modalBackdrop) {
        closeConcernsModal();
      }
    });
  }

  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modalBackdrop && !modalBackdrop.hidden) {
      closeConcernsModal();
    }
  });

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      filterConcerns(e.target.value);
    });
  }

  // Handle click on any concern inside modal
  modalItems.forEach((item) => {
    item.addEventListener("click", () => {
      const sym = item.dataset.symptom;
      if (symptomsInput && sym) {
        symptomsInput.value = sym;
        closeConcernsModal();
        symptomsInput.scrollIntoView({ behavior: "smooth", block: "center" });
        setTimeout(() => symptomsInput.focus(), 300);
      }
    });
  });
});
