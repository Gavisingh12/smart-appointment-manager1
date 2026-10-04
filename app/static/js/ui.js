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
      const options = { weekday: "long", day: "numeric", month: "long", year: "numeric" };
      dateEl.textContent = new Intl.DateTimeFormat(undefined, options).format(new Date());
    } catch (e) {
      dateEl.textContent = new Date().toDateString();
    }
  }

  // 2. Quick-Add Symptom Chips
  const symptomInput = document.getElementById("symptoms");
  document.querySelectorAll(".chip-btn").forEach((chip) => {
    chip.addEventListener("click", () => {
      if (!symptomInput) return;
      const symptom = chip.dataset.symptom || chip.textContent.trim();
      const currentVal = symptomInput.value.trim();
      if (!currentVal) {
        symptomInput.value = `${symptom}, `;
      } else if (!currentVal.toLowerCase().includes(symptom.toLowerCase())) {
        symptomInput.value = `${currentVal}${currentVal.endsWith(",") ? " " : ", "}${symptom}, `;
      }
      symptomInput.focus();
    });
  });

  // 3. Mobile Navigation Menu Toggle
  const navToggle = document.querySelector(".mobile-nav-toggle");
  const navLinks = document.querySelector(".nav-links");
  if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => {
      const isOpen = navLinks.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  }
});
