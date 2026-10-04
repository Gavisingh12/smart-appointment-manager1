document.addEventListener("DOMContentLoaded", () => {
  // 1. Time-of-Day Greeting and Local Date
  const greetingEl = document.getElementById("dashboard-greeting");
  if (greetingEl) {
    const rawName = greetingEl.dataset.name || "there";
    const hour = new Date().getHours();
    let timeGreeting = "Hello";
    if (hour >= 4 && hour < 12) {
      timeGreeting = "Good morning";
    } else if (hour >= 12 && hour < 17) {
      timeGreeting = "Good afternoon";
    } else {
      timeGreeting = "Good evening";
    }
    greetingEl.textContent = `${timeGreeting}, ${rawName}`;
  }

  const dateEl = document.getElementById("dashboard-date");
  if (dateEl) {
    try {
      const options = {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric",
        timeZone: "Asia/Kolkata"
      };
      dateEl.textContent = new Intl.DateTimeFormat("en-IN", options).format(new Date());
    } catch (e) {
      dateEl.textContent = new Date().toLocaleDateString(undefined, {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric"
      });
    }
  }

  // 2. Quick Symptom Chips (Accessible Toggle Buttons)
  const symptomInput = document.getElementById("symptoms");
  const chips = document.querySelectorAll(".chip-btn");
  if (symptomInput && chips.length > 0) {
    const updateChipStates = () => {
      const text = (symptomInput.value || "").toLowerCase();
      chips.forEach((chip) => {
        const val = (chip.dataset.symptom || chip.textContent).trim().toLowerCase();
        const isPresent = text.includes(val);
        chip.setAttribute("aria-pressed", isPresent ? "true" : "false");
      });
    };

    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        const symptom = chip.dataset.symptom || chip.textContent.trim();
        const currentVal = symptomInput.value.trim();
        const isPressed = chip.getAttribute("aria-pressed") === "true";

        if (isPressed) {
          // Remove symptom from textarea
          const regex = new RegExp(`\\b${symptom}\\b,?\\s*`, "i");
          symptomInput.value = currentVal.replace(regex, "").replace(/,\s*,/g, ",").trim();
          chip.setAttribute("aria-pressed", "false");
        } else {
          // Append symptom to textarea
          if (!currentVal) {
            symptomInput.value = `${symptom}, `;
          } else if (!currentVal.toLowerCase().includes(symptom.toLowerCase())) {
            symptomInput.value = `${currentVal}${currentVal.endsWith(",") ? " " : ", "}${symptom}, `;
          }
          chip.setAttribute("aria-pressed", "true");
        }
        symptomInput.focus();
      });
    });

    symptomInput.addEventListener("input", updateChipStates);
    updateChipStates();
  }

  // 3. Mobile Navigation Menu Toggle
  const navToggle = document.querySelector(".mobile-nav-toggle");
  const navLinks = document.querySelector(".nav-links");
  if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => {
      const isOpen = navLinks.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  }

  // 4. Appointments Segmented Tab Filter (Upcoming vs All)
  const tabUpcoming = document.getElementById("tab-upcoming");
  const tabAll = document.getElementById("tab-all");
  const appointmentsContainer = document.getElementById("appointmentsContainer");

  if (tabUpcoming && tabAll && appointmentsContainer) {
    const filterAppointments = (onlyUpcoming) => {
      const cards = appointmentsContainer.querySelectorAll(".appointment-card");
      cards.forEach((card) => {
        const isUpcoming = card.dataset.upcoming === "true";
        if (onlyUpcoming && !isUpcoming) {
          card.style.display = "none";
        } else {
          card.style.display = "flex";
        }
      });
    };

    tabUpcoming.addEventListener("click", () => {
      tabUpcoming.setAttribute("aria-selected", "true");
      tabAll.setAttribute("aria-selected", "false");
      filterAppointments(true);
    });

    tabAll.addEventListener("click", () => {
      tabAll.setAttribute("aria-selected", "true");
      tabUpcoming.setAttribute("aria-selected", "false");
      filterAppointments(false);
    });

    // Default to upcoming view
    filterAppointments(true);
  }

  // 5. Accessible Remove/Delete Dialog Modal
  const dialog = document.getElementById("deleteAppointmentDialog");
  const cancelBtn = document.getElementById("cancelDialogBtn");
  const confirmBtn = document.getElementById("confirmDeleteBtn");
  let formToSubmit = null;

  if (dialog && cancelBtn && confirmBtn) {
    document.querySelectorAll(".trigger-delete-dialog").forEach((button) => {
      button.addEventListener("click", (e) => {
        formToSubmit = button.closest("form");
        const doctorName = button.dataset.doctor || "this item";
        const appDate = button.dataset.date || "";

        const nameSpan = document.getElementById("dialog-doctor-name");
        if (nameSpan) nameSpan.textContent = doctorName;

        const dateSpan = document.getElementById("dialog-appointment-date");
        if (dateSpan) dateSpan.textContent = appDate;

        if (typeof dialog.showModal === "function") {
          dialog.showModal();
        } else {
          // Fallback if dialog tag not supported
          if (confirm(`Remove appointment with ${doctorName} on ${appDate}?`)) {
            if (formToSubmit) formToSubmit.submit();
          }
        }
      });
    });

    cancelBtn.addEventListener("click", () => {
      dialog.close();
      formToSubmit = null;
    });

    confirmBtn.addEventListener("click", () => {
      if (formToSubmit) {
        formToSubmit.submit();
      }
    });

    dialog.addEventListener("cancel", () => {
      formToSubmit = null;
    });
  }
});
