/* ============================================================
   settings.js
   Behavior for the Settings page:
   - Live preview of newly-selected profile photo
   - Confirmation dialog before deleting account (safety net for
     a destructive, irreversible action)
   - Highlight the active section in the side nav while scrolling
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    /* ---------------------------------------------------------
       LIVE PROFILE IMAGE PREVIEW
       --------------------------------------------------------- */
    const fileInput = document.getElementById("profile_image");
    const preview = document.getElementById("settingsImagePreview");

    if (fileInput && preview) {
        fileInput.addEventListener("change", () => {
            const file = fileInput.files[0];
            if (!file) return;

            if (file.size > 3 * 1024 * 1024) {
                alert("Please choose an image smaller than 3MB.");
                fileInput.value = "";
                return;
            }

            const reader = new FileReader();
            reader.onload = (e) => {
                preview.innerHTML = `<img src="${e.target.result}" alt="Profile preview">`;
            };
            reader.readAsDataURL(file);
        });
    }

    /* ---------------------------------------------------------
       DELETE ACCOUNT CONFIRMATION
       A destructive, irreversible action always deserves a
       confirmation step before submitting.
       --------------------------------------------------------- */
    const deleteBtn = document.getElementById("deleteAccountBtn");
    const deleteForm = document.getElementById("deleteAccountForm");

    if (deleteBtn && deleteForm) {
        deleteBtn.addEventListener("click", () => {
            const confirmed = confirm(
                "Are you sure you want to permanently delete your account? This cannot be undone."
            );
            if (confirmed) {
                deleteForm.submit();
            }
        });
    }

    /* ---------------------------------------------------------
       SETTINGS SIDE-NAV: highlight active section while scrolling
       --------------------------------------------------------- */
    const navLinks = document.querySelectorAll(".settings-nav a");
    const sections = document.querySelectorAll(".settings-section");

    if (navLinks.length && sections.length && "IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute("id");
                    navLinks.forEach(link => {
                        link.classList.toggle("active", link.getAttribute("href") === `#${id}`);
                    });
                }
            });
        }, { rootMargin: "-40% 0px -50% 0px" });

        sections.forEach(section => observer.observe(section));
    }

});
