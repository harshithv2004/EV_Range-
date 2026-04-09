/**
 * EV Range Predictor — main.js
 * Handles: form UX, loading state, client-side validation feedback
 */

document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('predictForm');
    const submitBtn = document.getElementById('submitBtn');

    if (!form || !submitBtn) return;

    const btnText   = submitBtn.querySelector('.btn-text');
    const btnIcon   = submitBtn.querySelector('.btn-icon');
    const btnLoader = submitBtn.querySelector('.btn-loader');

    // ── Loading state on submit ───────────────────
    form.addEventListener('submit', (e) => {
        if (!form.checkValidity()) {
            e.preventDefault();
            highlightInvalid();
            return;
        }

        // Show loader
        btnText.style.display   = 'none';
        btnIcon.style.display   = 'none';
        btnLoader.style.display = 'flex';
        submitBtn.classList.add('loading');
    });

    // ── Highlight invalid fields on submit attempt ─
    function highlightInvalid() {
        const inputs = form.querySelectorAll('input[required], select[required]');
        inputs.forEach(input => {
            if (!input.validity.valid) {
                input.style.borderColor = '#f87171';
                input.addEventListener('input', () => {
                    input.style.borderColor = '';
                }, { once: true });
            }
        });

        // Scroll to first invalid
        const first = form.querySelector(':invalid');
        if (first) {
            first.scrollIntoView({ behavior: 'smooth', block: 'center' });
            first.focus();
        }
    }

    // ── Live number formatting feedback ───────────
    const numberInputs = form.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        const min = parseFloat(input.min);
        const max = parseFloat(input.max);
        const hint = input.closest('.input-group')?.querySelector('.hint');

        input.addEventListener('input', () => {
            const val = parseFloat(input.value);
            if (isNaN(val)) return;

            if (val < min || val > max) {
                input.style.borderColor = 'rgba(251,191,36,0.6)';
                if (hint) hint.style.color = '#fbbf24';
            } else {
                input.style.borderColor = '';
                if (hint) hint.style.color = '';
            }
        });
    });

    // ── Staggered section reveal on load ──────────
    const sections = document.querySelectorAll('.form-section');
    sections.forEach((section, i) => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(16px)';
        section.style.transition = `opacity 0.4s ease ${i * 0.08}s, transform 0.4s ease ${i * 0.08}s`;
        setTimeout(() => {
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }, 50);
    });

    // ── Auto-scroll to error banner if present ────
    const errorBanner = document.getElementById('errorBanner');
    if (errorBanner) {
        errorBanner.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
});
