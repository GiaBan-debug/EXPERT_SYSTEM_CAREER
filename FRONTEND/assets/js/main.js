/**
 * MAIN SCRIPTS
 * Theme toggling, header scroll state, mobile navigation, global toast
 */

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initHeader();
  initMobileMenu();
  renderUserAuthNav();
});

// Hiển thị trạng thái đăng nhập trên Header
function renderUserAuthNav() {
  const navActions = document.querySelector(".nav-actions");
  if (!navActions) return;

  const currentUser = typeof ApiClient !== "undefined" && ApiClient.getCurrentUser ? ApiClient.getCurrentUser() : null;

  // Xóa nút login cũ nếu có
  const oldAuthBox = document.getElementById("headerAuthBox");
  if (oldAuthBox) oldAuthBox.remove();

  const authBox = document.createElement("div");
  authBox.id = "headerAuthBox";
  authBox.style.display = "flex";
  authBox.style.alignItems = "center";
  authBox.style.gap = "0.6rem";

  // Xác định tiền tố đường dẫn (nếu đang ở trang gốc index.html hay ở trong pages/)
  const isPagesDir = window.location.pathname.includes("/pages/");
  const loginUrl = isPagesDir ? "login.html" : "pages/login.html";
  const registerUrl = isPagesDir ? "register.html" : "pages/register.html";
  const adminUrl = isPagesDir ? "admin.html" : "pages/admin.html";

  if (currentUser) {
    const roleBadge = currentUser.role === "admin"
      ? '<span class="role-badge-pill role-badge-admin">Admin</span>'
      : '<span class="role-badge-pill role-badge-user">Học sinh</span>';

    authBox.innerHTML = `
      <div class="user-profile-btn" id="btnUserMenu" title="Tài khoản hiện tại">
        <i class="fas fa-user-circle" style="color: var(--primary-600); font-size: 1.1rem;"></i>
        <span>${currentUser.fullName || currentUser.username}</span>
        ${roleBadge}
      </div>
      <button class="btn btn-secondary btn-sm" id="btnLogoutHeader" title="Đăng xuất" style="padding: 0.4rem 0.65rem;">
        <i class="fas fa-sign-out-alt"></i>
      </button>
    `;

    // Nếu là admin, hiển thị link Admin trên menu
    const adminLink = document.getElementById("nav-admin") || document.querySelector('a[href*="admin.html"]');
    if (adminLink) {
      adminLink.style.display = "inline-flex";
    }

    navActions.prepend(authBox);

    document.getElementById("btnLogoutHeader")?.addEventListener("click", () => {
      if (confirm("Bạn có chắc chắn muốn đăng xuất không?")) {
        ApiClient.logout();
      }
    });

    document.getElementById("btnUserMenu")?.addEventListener("click", () => {
      if (currentUser.role === "admin") {
        window.location.href = adminUrl;
      }
    });
  } else {
    authBox.innerHTML = `
      <a href="${loginUrl}" class="btn btn-secondary btn-sm" style="display: flex; align-items: center; gap: 0.35rem;">
        <i class="fas fa-sign-in-alt"></i> <span>Đăng nhập</span>
      </a>
    `;

    // Nếu chưa đăng nhập admin thì ẩn link admin trên header công cộng
    const adminLink = document.getElementById("nav-admin") || document.querySelector('a[href*="admin.html"]');
    if (adminLink) {
      adminLink.style.display = "none";
    }

    navActions.prepend(authBox);
  }
}

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
