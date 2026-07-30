/* ============================================================
   landing.js
   Landing-page-only behavior: animated count-up numbers for the
   Community Statistics section. Numbers count up from 0 to their
   target value once the section scrolls into view.
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    const statNumbers = document.querySelectorAll(".stat-number");
    if (statNumbers.length === 0) return;

    /**
     * Animates a single number element counting up from 0 to `target`.
     * Uses requestAnimationFrame for a smooth, performant animation.
     */
    function animateCount(el, target, duration = 1500) {
        const startTime = performance.now();

        function tick(now) {
            const progress = Math.min((now - startTime) / duration, 1);
            // easeOutQuad easing for a natural deceleration
            const eased = 1 - (1 - progress) * (1 - progress);
            const current = Math.floor(eased * target);
            el.textContent = current.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(tick);
            } else {
                el.textContent = target.toLocaleString();
            }
        }
        requestAnimationFrame(tick);
    }

    // Only trigger the count-up once, when the stats section enters view
    const statsSection = document.querySelector(".stats-section");
    if (statsSection && "IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    statNumbers.forEach(el => {
                        const target = parseInt(el.dataset.count, 10) || 0;
                        animateCount(el, target);
                    });
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.4 });

        observer.observe(statsSection);
    }

});
