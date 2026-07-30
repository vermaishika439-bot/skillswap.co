/* ============================================================
   theme.js
   Handles dark/light mode. Runs BEFORE other scripts (loaded
   early in base.html) to avoid a flash of the wrong theme.
   Preference is saved in localStorage so it persists across
   page loads without needing a server round-trip.
   ============================================================ */

(function () {
    const savedTheme = localStorage.getItem("skillswap-theme");

    // Apply saved theme immediately (before page paints)
    if (savedTheme === "dark") {
        document.body.classList.add("dark-theme");
    }

    // Expose a global toggle function used by the Settings page switch
    window.toggleDarkMode = function (isDark) {
        if (isDark) {
            document.body.classList.add("dark-theme");
            localStorage.setItem("skillswap-theme", "dark");
        } else {
            document.body.classList.remove("dark-theme");
            localStorage.setItem("skillswap-theme", "light");
        }
    };

    // On page load, sync any dark-mode toggle switch UI to match saved state
    document.addEventListener("DOMContentLoaded", () => {
        const toggle = document.getElementById("darkModeToggle");
        if (toggle) {
            toggle.checked = document.body.classList.contains("dark-theme");
            toggle.addEventListener("change", (e) => {
                window.toggleDarkMode(e.target.checked);
            });
        }
    });
})();
