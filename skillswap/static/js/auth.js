/* ============================================================
   auth.js
   Behavior for Login and Signup pages:
   - Password show/hide toggle
   - Live preview of uploaded profile picture on signup
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    /* ---------------------------------------------------------
       PASSWORD SHOW/HIDE TOGGLE
       --------------------------------------------------------- */
    document.querySelectorAll(".password-toggle").forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.dataset.target;
            const input = document.getElementById(targetId);
            if (!input) return;

            const isHidden = input.type === "password";
            input.type = isHidden ? "text" : "password";

            // Swap the eye icon to an "eye-off" style path when revealed
            btn.innerHTML = isHidden
                ? `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.94 10.94 0 0 1 12 20c-7 0-11-8-11-8a18.6 18.6 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>`
                : `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`;
        });
    });

    /* ---------------------------------------------------------
       LIVE PROFILE IMAGE PREVIEW (Signup page)
       --------------------------------------------------------- */
    const fileInput = document.getElementById("profile_image");
    const preview = document.getElementById("imagePreview");

    if (fileInput && preview) {
        fileInput.addEventListener("change", () => {
            const file = fileInput.files[0];
            if (!file) return;

            // Basic client-side size check (3MB limit, matches server-side config)
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

});
