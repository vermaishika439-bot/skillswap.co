/* ============================================================
   swap-requests.js
   Handles switching between the Incoming / Outgoing / Pending /
   Accepted / Rejected tabs on the Swap Requests page. Pure
   client-side tab switching — all the data for every tab is
   already rendered in the page, we just show/hide panels.
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
    const tabButtons = document.querySelectorAll("#swapTabs .tab-btn");
    const panels = document.querySelectorAll(".swap-tab-panel");

    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const target = btn.dataset.tab;

            // Update active state on buttons
            tabButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            // Show only the matching panel
            panels.forEach(panel => {
                panel.classList.toggle("active", panel.id === `panel-${target}`);
            });
        });
    });
});
