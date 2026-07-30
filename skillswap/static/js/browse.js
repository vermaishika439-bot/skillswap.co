/* ============================================================
   browse.js
   Small enhancements for the Browse Skills page. Filtering and
   pagination are handled server-side (Flask) via query params
   for simplicity and reliability — this file just adds small
   UX touches on top.
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    // Add a subtle fade-in to skill cards as they render, so the
    // grid doesn't feel like it "pops" in instantly on filter change
    const cards = document.querySelectorAll(".skill-card");
    cards.forEach((card, index) => {
        card.style.opacity = "0";
        card.style.transform = "translateY(12px)";
        setTimeout(() => {
            card.style.transition = "opacity 0.4s ease, transform 0.4s ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, index * 40); // slight stagger for a polished feel
    });

});
