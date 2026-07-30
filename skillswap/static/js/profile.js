/* ============================================================
   profile.js
   Handles the "Send Swap Request" modal on the profile page:
   closing it by clicking the overlay or pressing Escape.
   (Opening is handled inline via onclick in profile.html, and
   the close button also uses an inline handler — this file adds
   the two extra convenience interactions.)
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("swapModal");
    if (!modal) return;

    // Click on the dark overlay (outside the card) closes the modal
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.classList.remove("open");
        }
    });

    // Escape key closes the modal
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            modal.classList.remove("open");
        }
    });
});
