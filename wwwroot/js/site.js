/**
 * HomeLedger — Premium Motion & Interaction Engine
 * Clean, lightweight, professional agency-grade interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSidebar();
  initScrollAnimations();
  initCounters();
  initTooltipsAndToggles();
});

/* ========================================================
   THEME TOGGLE (DARK / LIGHT WITH SMOOTH TRANSITION)
   ======================================================== */
function initTheme() {
  const themeToggle = document.getElementById('themeToggle');
  const storedTheme = localStorage.getItem('homeledger_theme');

  if (storedTheme === 'light') {
    document.body.classList.add('light-mode');
    updateThemeIcon(true);
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const isLight = document.body.classList.toggle('light-mode');
      localStorage.setItem('homeledger_theme', isLight ? 'light' : 'dark');
      updateThemeIcon(isLight);
    });
  }
}

function updateThemeIcon(isLight) {
  const icon = document.querySelector('#themeToggle i');
  if (icon) {
    icon.className = isLight ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
  }
}

/* ========================================================
   MOBILE & DESKTOP SIDEBAR DRAWER
   ======================================================== */
function initSidebar() {
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('appSidebar');
  const overlay = document.getElementById('sidebarOverlay');

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('show');
      if (overlay) overlay.classList.toggle('show');
    });
  }

  if (overlay) {
    overlay.addEventListener('click', () => {
      if (sidebar) sidebar.classList.remove('show');
      overlay.classList.remove('show');
    });
  }
}

/* ========================================================
   SCROLL-TRIGGERED REVEAL ANIMATIONS
   ======================================================== */
function initScrollAnimations() {
  const elements = document.querySelectorAll('.reveal-on-scroll');
  if (!elements.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );

  elements.forEach((el) => observer.observe(el));
}

/* ========================================================
   INTERACTIVE KPI NUMERICAL COUNTERS
   ======================================================== */
function initCounters() {
  const counters = document.querySelectorAll('[data-counter]');
  if (!counters.length) return;

  counters.forEach((counter) => {
    const target = parseFloat(counter.getAttribute('data-counter') || '0');
    const prefix = counter.getAttribute('data-prefix') || '';
    const decimals = parseInt(counter.getAttribute('data-decimals') || '2', 10);
    const duration = 1200; // 1.2s smooth reveal
    const startTime = performance.now();

    function updateCounter(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease out cubic
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      const currentVal = target * easeProgress;

      counter.textContent =
        prefix +
        currentVal.toLocaleString('en-IN', {
          minimumFractionDigits: decimals,
          maximumFractionDigits: decimals,
        });

      if (progress < 1) {
        requestAnimationFrame(updateCounter);
      }
    }

    requestAnimationFrame(updateCounter);
  });
}

/* ========================================================
   PASSWORD TOGGLES & HELPER SHORTCUTS
   ======================================================== */
function initTooltipsAndToggles() {
  window.togglePassword = function (inputId, iconId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
    if (!input || !icon) return;

    if (input.type === 'password') {
      input.type = 'text';
      icon.className = 'fa-solid fa-eye-slash';
    } else {
      input.type = 'password';
      icon.className = 'fa-solid fa-eye';
    }
  };
}
