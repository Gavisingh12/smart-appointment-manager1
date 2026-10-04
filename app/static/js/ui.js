document.addEventListener("DOMContentLoaded", () => {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-revealed");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 },
  );

  document.querySelectorAll(".panel, .metric-card, .feature-card, .activity-card, .trust-card, .auth-card").forEach((element) => {
    revealObserver.observe(element);
  });
});
