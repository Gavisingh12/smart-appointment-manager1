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
        year: "numeric"
      };
      dateEl.textContent = new Intl.DateTimeFormat(undefined, options).format(new Date());
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
        const val = (chip.dataset.symptom || chip.textContent).replace(/^\+\s*/, "").trim().toLowerCase();
        const isPresent = text.includes(val);
        chip.setAttribute("aria-pressed", isPresent ? "true" : "false");
      });
    };

    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        const symptom = (chip.dataset.symptom || chip.textContent).replace(/^\+\s*/, "").trim();
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
        updateWordCount();
      });
    });

    const wordCountEl = document.getElementById("symptomWordCount");
    const updateWordCount = () => {
      if (!wordCountEl) return;
      const text = symptomInput.value.trim();
      const words = text ? text.split(/\s+/).length : 0;
      wordCountEl.textContent = `${words} word${words !== 1 ? 's' : ''} logged`;
    };

    symptomInput.addEventListener("input", () => {
      updateChipStates();
      updateWordCount();
    });
    updateChipStates();
    updateWordCount();
  }

  // 3. "Check Symptoms" Prominent Sidebar Action Handler
  const checkSymptomsBtn = document.getElementById("sidebarCheckSymptomsBtn");
  if (checkSymptomsBtn && symptomInput) {
    checkSymptomsBtn.addEventListener("click", (e) => {
      if (window.location.pathname.includes("/dashboard") || window.location.pathname === "/") {
        e.preventDefault();
        symptomInput.scrollIntoView({ behavior: "smooth", block: "center" });
        setTimeout(() => symptomInput.focus(), 300);
      }
    });
  }

  // 3b. Common Health Concerns Card Clicks
  const concernCards = document.querySelectorAll(".concern-card[data-symptom]");
  concernCards.forEach((card) => {
    card.addEventListener("click", () => {
      const sym = card.dataset.symptom;
      if (symptomInput && sym) {
        symptomInput.value = sym;
        symptomInput.scrollIntoView({ behavior: "smooth", block: "center" });
        setTimeout(() => symptomInput.focus(), 250);
      }
    });
  });

  const startConsultationBannerBtn = document.getElementById("startConsultationBannerBtn");
  if (startConsultationBannerBtn && symptomInput) {
    startConsultationBannerBtn.addEventListener("click", () => {
      symptomInput.scrollIntoView({ behavior: "smooth", block: "center" });
      setTimeout(() => symptomInput.focus(), 250);
    });
  }


  // 4. Mobile Bottom Nav "More" Sheet Modal
  const moreTrigger = document.getElementById("mobileMoreTrigger");
  const drawer = document.getElementById("mobileDrawer");
  const drawerBackdrop = document.getElementById("mobileDrawerBackdrop");
  const drawerClose = document.getElementById("mobileDrawerClose");

  if (moreTrigger && drawer && drawerBackdrop) {
    const openDrawer = () => {
      drawer.hidden = false;
      drawerBackdrop.hidden = false;
      drawer.classList.add("is-open");
      drawerBackdrop.classList.add("is-open");
      moreTrigger.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
    };

    const closeDrawer = () => {
      drawer.classList.remove("is-open");
      drawerBackdrop.classList.remove("is-open");
      setTimeout(() => {
        drawer.hidden = true;
        drawerBackdrop.hidden = true;
      }, 200);
      moreTrigger.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    };

    moreTrigger.addEventListener("click", () => {
      if (drawer.classList.contains("is-open")) {
        closeDrawer();
      } else {
        openDrawer();
      }
    });

    if (drawerClose) drawerClose.addEventListener("click", closeDrawer);
    drawerBackdrop.addEventListener("click", closeDrawer);
    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && drawer.classList.contains("is-open")) {
        closeDrawer();
      }
    });
  }

  // 5. Appointments Segmented Tab Filter (Upcoming vs All)
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

    filterAppointments(true);
  }

  // 6. Accessible Remove/Delete Dialog Modal
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

  // 7. Desktop Sidebar Collapse & Hover-to-Expand Toggle
  const appSidebar = document.getElementById("appSidebar");
  const appLayout = document.querySelector(".app-layout");
  const sidebarCollapseBtn = document.getElementById("sidebarCollapseBtn");

  if (appSidebar && appLayout) {
    const applySidebarState = (collapsed) => {
      appSidebar.classList.toggle("is-collapsed", collapsed);
      appLayout.classList.toggle("sidebar-collapsed", collapsed);
      const label = collapsed ? "Expand sidebar" : "Collapse sidebar";
      if (sidebarCollapseBtn) {
        sidebarCollapseBtn.setAttribute("title", label);
        sidebarCollapseBtn.setAttribute("aria-label", label);
      }
      try {
        localStorage.setItem("cc_sidebar_collapsed", collapsed ? "true" : "false");
        document.cookie = "cc_sidebar_collapsed=" + (collapsed ? "1" : "0") + "; path=/; max-age=31536000; SameSite=Lax";
      } catch (e) {}
    };

    // Keep state synced with cookie / localStorage without flash
    try {
      const match = document.cookie.match(/(?:^|; )cc_sidebar_collapsed=([^;]*)/);
      const isCol = match ? (match[1] === "1") : (localStorage.getItem("cc_sidebar_collapsed") === "true");
      if (isCol !== appSidebar.classList.contains("is-collapsed")) {
        applySidebarState(isCol);
      }
    } catch (e) {}

    const toggleSidebar = () => {
      const isCurrentlyCollapsed = appSidebar.classList.contains("is-collapsed");
      applySidebarState(!isCurrentlyCollapsed);
    };

    if (sidebarCollapseBtn) {
      sidebarCollapseBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        toggleSidebar();
      });
    }
  }

  // Remove preload class after first render to ensure silky smooth transitions
  requestAnimationFrame(() => {
    document.body.classList.remove("preload");
  });
});
