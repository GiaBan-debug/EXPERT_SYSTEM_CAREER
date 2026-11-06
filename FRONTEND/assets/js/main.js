/**
 * MAIN SCRIPTS
 * Theme toggling, header scroll state, mobile navigation, global toast
 */

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initHeader();
  initMobileMenu();
});

// Chuyển đổi Dark / Light Theme
function initTheme() {
  const savedTheme = localStorage.getItem("career_theme") || "light";
  document.documentElement.setAttribute("data-theme", savedTheme);
  updateThemeIcon(savedTheme);

  const toggleBtns = document.querySelectorAll(".theme-toggle-btn");
  toggleBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme");
      const next = current === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("career_theme", next);
      updateThemeIcon(next);
    });
  });
}

function updateThemeIcon(theme) {
  const icons = document.querySelectorAll(".theme-toggle-btn i");
  icons.forEach(icon => {
    if (theme === "dark") {
      icon.className = "fas fa-sun";
    } else {
      icon.className = "fas fa-moon";
    }
  });
}

// Hiệu ứng Header khi cuộn trang
function initHeader() {
  const header = document.querySelector(".app-header");
  if (!header) return;

  window.addEventListener("scroll", () => {
    if (window.scrollY > 20) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  });
}

// Mobile menu toggle
function initMobileMenu() {
  const btn = document.querySelector(".mobile-menu-btn");
  const nav = document.querySelector(".nav-links");
  if (!btn || !nav) return;

  btn.addEventListener("click", () => {
    nav.classList.toggle("show");
  });
}

// Global Toast notification
function showToast(message, type = "info") {
  let container = document.querySelector(".toast-container");
  if (!container) {
    container = document.createElement("div");
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  
  let iconClass = "fa-info-circle";
  if (type === "success") iconClass = "fa-check-circle";
  if (type === "warning") iconClass = "fa-exclamation-triangle";
  if (type === "error") iconClass = "fa-times-circle";

  toast.innerHTML = `
    <i class="fas ${iconClass}" style="margin-top: 2px;"></i>
    <div style="flex:1;">
      <p style="font-weight:600; font-size:0.9rem;">${message}</p>
    </div>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = "fadeOut 0.3s forwards";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}
