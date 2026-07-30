/* ============================================================
   main.js
   Global behaviors that run on every page:
   - Navbar background change on scroll
   - Mobile hamburger menu toggle
   - Scroll-reveal animations (fade + rise into view)
   - Auto-dismiss flash messages after a few seconds
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    /* ---------------------------------------------------------
       1. NAVBAR: add "scrolled" class once the page scrolls down
       --------------------------------------------------------- */
    const navbar = document.getElementById("navbar");
    if (navbar) {
        const handleScroll = () => {
            if (window.scrollY > 20) {
                navbar.classList.add("scrolled");
            } else {
                navbar.classList.remove("scrolled");
            }
        };
        window.addEventListener("scroll", handleScroll);
        handleScroll(); // run once on load in case page is already scrolled
    }

    /* ---------------------------------------------------------
       2. MOBILE MENU TOGGLE
       --------------------------------------------------------- */
    const navToggle = document.getElementById("navbarToggle");
    const navLinks = document.getElementById("navbarLinks");
    if (navToggle && navLinks) {
        navToggle.addEventListener("click", () => {
            navLinks.classList.toggle("open");
        });
        // Close menu when a link is clicked (better mobile UX)
        navLinks.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", () => navLinks.classList.remove("open"));
        });
    }

    /* ---------------------------------------------------------
       3. SCROLL-REVEAL ANIMATIONS
       Any element with class="reveal" fades + rises into view
       the first time it enters the viewport.
       --------------------------------------------------------- */
    const revealElements = document.querySelectorAll(".reveal");
    if (revealElements.length > 0 && "IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target); // only animate once
                }
            });
        }, { threshold: 0.15 });

        revealElements.forEach(el => observer.observe(el));
    } else {
        // Fallback: just show everything if IntersectionObserver isn't supported
        revealElements.forEach(el => el.classList.add("visible"));
    }

    /* ---------------------------------------------------------
       4. AUTO-DISMISS FLASH MESSAGES after 4 seconds
       --------------------------------------------------------- */
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.4s ease, transform 0.4s ease";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-10px)";
            setTimeout(() => alert.remove(), 400);
        }, 4000);
    });

});
