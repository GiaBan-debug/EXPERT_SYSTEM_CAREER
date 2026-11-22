/**
 * ADMIN DASHBOARD & KNOWLEDGE BASE CONTROLLER
 */

let allRulesCache = [];

document.addEventListener("DOMContentLoaded", () => {
  // KIỂM TRA PHÂN QUYỀN ADMIN (ROUTE GUARD)
  const currentUser = typeof ApiClient !== "undefined" && ApiClient.getCurrentUser ? ApiClient.getCurrentUser() : null;
  if (!currentUser || currentUser.role !== "admin") {
    alert("CẢNH BÁO: Bạn cần đăng nhập bằng tài khoản QUẢN TRỊ VIÊN (Admin) để truy cập trang này!");
    window.location.href = "login.html";
    return;
  }

  initAdminTabs();
  loadAdminDashboard();
  initModalActions();
  initFilterActions();
});

// Chuyển đổi tab
function initAdminTabs() {
  const tabBtns = document.querySelectorAll(".admin-tab-btn");
  const tabPanes = document.querySelectorAll(".admin-tab-pane");

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      tabPanes.forEach(p => p.classList.remove("active"));

      btn.classList.add("active");
      const targetId = btn.dataset.tab;
      const targetPane = document.getElementById(targetId);
      if (targetPane) targetPane.classList.add("active");
    });
  });
}

// Nạp dữ liệu thống kê & tập luật
async function loadAdminDashboard() {
  try {
    const stats = await ApiClient.getAdminStats();
    renderStats(stats);
    renderRecentConsultations(stats.recentConsultations || []);

    const rules = await ApiClient.getAdminRules();
    allRulesCache = rules;
    renderRulesTable(rules);
  } catch (err) {
    console.error("Lỗi nạp dashboard admin:", err);
    showToast("Không thể tải toàn bộ dữ liệu quản trị", "warning");
  }
}

// Hiển thị số liệu
function renderStats(stats) {
  if (stats.rules) {
    document.getElementById("statTotalRules").textContent = stats.rules.total || 35;
    document.getElementById("statActiveRules").textContent = `${stats.rules.enabled || 35} đang kích hoạt`;
  }
  if (stats.totalConsultations !== undefined) {
    document.getElementById("statTotalConsultations").textContent = stats.totalConsultations;
  }
  if (stats.totalCareers !== undefined) {
    document.getElementById("statTotalCareers").textContent = stats.totalCareers;
  }
}

// Hiển thị bảng luật
function renderRulesTable(rules) {
  const tbody = document.getElementById("rulesTableBody");
  if (!tbody) return;

  if (rules.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 2.5rem; color: var(--text-muted);">Không tìm thấy luật nào phù hợp.</td></tr>`;
    return;
  }

  let html = "";
  rules.forEach(rule => {
    const categoryBadge = rule.category === "ability" 
      ? '<span class="badge badge-primary">Năng lực</span>'
      : (rule.category === "interest" 
          ? '<span class="badge badge-purple">Sở thích</span>' 
          : '<span class="badge badge-success">Nhóm ngành</span>');

    const isChecked = rule.enabled ? "checked" : "";

    html += `
      <tr>
        <td><strong style="color: var(--primary-600);">${rule.id}</strong></td>
        <td>
          <div style="font-weight: 700; color: var(--text-main);">${rule.name}</div>
          <small style="color: var(--text-muted); font-size: 0.8rem;">${rule.description || "Chưa có mô tả"}</small>
        </td>
        <td>${categoryBadge}</td>
        <td style="text-align: center;"><span class="badge badge-warning">${rule.priority}</span></td>
        <td style="text-align: center;"><strong>${rule.confidence}</strong></td>
        <td style="text-align: center;">
          <label class="switch">
            <input type="checkbox" ${isChecked} onchange="toggleRuleState('${rule.id}')">
            <span class="slider-switch"></span>
          </label>
        </td>
        <td style="text-align: right;">
          <button class="btn btn-secondary btn-sm" onclick="deleteRule('${rule.id}')" title="Xóa luật">
            <i class="fas fa-trash-alt" style="color: var(--accent-rose);"></i>
          </button>
        </td>
      </tr>
    `;
  });

  tbody.innerHTML = html;
}

// Bật/tắt trạng thái luật
window.toggleRuleState = async function(ruleId) {
  try {
    const res = await ApiClient.toggleRule(ruleId);
    showToast(res.message || `Đã cập nhật trạng thái luật ${ruleId}`, "success");
    // Cập nhật lại cache
    const target = allRulesCache.find(r => r.id === ruleId);
    if (target) target.enabled = !target.enabled;
  } catch (err) {
    showToast("Lỗi khi thay đổi trạng thái luật", "error");
  }
};

// Xóa luật
window.deleteRule = async function(ruleId) {
  if (!confirm(`Bạn có chắc chắn muốn xóa luật ${ruleId} khỏi cơ sở tri thức không?`)) return;
  try {
    await ApiClient.deleteRule(ruleId);
    showToast(`Đã xóa thành công luật ${ruleId}`, "success");
    allRulesCache = allRulesCache.filter(r => r.id !== ruleId);
    renderRulesTable(allRulesCache);
  } catch (err) {
    showToast("Lỗi xóa luật", "error");
  }
};

// Hiển thị lịch sử tư vấn gần đây
function renderRecentConsultations(list) {
  const tbody = document.getElementById("recentConsultationsTableBody");
  if (!tbody) return;

  if (list.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 2rem; color: var(--text-muted);">Chưa có lượt tư vấn nào ghi nhận trong CSDL.</td></tr>`;
    return;
  }

  let html = "";
  list.forEach(item => {
    html += `
      <tr>
        <td><strong>${item.id}</strong></td>
        <td>${item.studentName}</td>
        <td><span class="badge badge-purple">${item.dominantCode || "IRC"}</span></td>
        <td><strong>${item.targetCareer}</strong></td>
        <td><span class="badge badge-success">${item.matchRate}%</span></td>
        <td><small style="color: var(--text-muted);">${item.createdAt || new Date().toLocaleDateString("vi-VN")}</small></td>
      </tr>
    `;
  });

  tbody.innerHTML = html;
}

// Bộ lọc tìm kiếm luật
function initFilterActions() {
  const searchInput = document.getElementById("ruleSearchInput");
  const categoryFilter = document.getElementById("ruleCategoryFilter");
  const refreshBtn = document.getElementById("btnRefreshRules");

  function applyFilter() {
    const q = searchInput ? searchInput.value.toLowerCase().trim() : "";
    const cat = categoryFilter ? categoryFilter.value : "ALL";

    const filtered = allRulesCache.filter(r => {
      const matchText = !q || r.id.toLowerCase().includes(q) || r.name.toLowerCase().includes(q) || (r.description && r.description.toLowerCase().includes(q));
      const matchCat = cat === "ALL" || r.category === cat;
      return matchText && matchCat;
    });

    renderRulesTable(filtered);
  }

  if (searchInput) searchInput.addEventListener("input", applyFilter);
  if (categoryFilter) categoryFilter.addEventListener("change", applyFilter);
  if (refreshBtn) refreshBtn.addEventListener("click", loadAdminDashboard);
}

// Modal thêm luật
function initModalActions() {
  const modal = document.getElementById("addRuleModal");
  const openBtn = document.getElementById("btnOpenAddRuleModal");
  const closeBtn = document.getElementById("btnCloseModal");
  const cancelBtn = document.getElementById("btnCancelModal");
  const addForm = document.getElementById("addRuleForm");

  function openModal() {
    if (modal) modal.style.display = "flex";
  }

  function closeModal() {
    if (modal) modal.style.display = "none";
  }

  if (openBtn) openBtn.addEventListener("click", openModal);
  if (closeBtn) closeBtn.addEventListener("click", closeModal);
  if (cancelBtn) cancelBtn.addEventListener("click", closeModal);

  if (addForm) {
    addForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      try {
        const conditions = JSON.parse(document.getElementById("newRuleConditions").value);
        const conclusion = JSON.parse(document.getElementById("newRuleConclusion").value);

        const newRule = {
          id: document.getElementById("newRuleId").value.trim().toUpperCase(),
          name: document.getElementById("newRuleName").value.trim(),
          description: document.getElementById("newRuleDesc").value.trim(),
          category: document.getElementById("newRuleCategory").value,
          priority: parseInt(document.getElementById("newRulePriority").value),
          confidence: parseFloat(document.getElementById("newRuleConfidence").value),
          conditions: conditions,
          conclusion: conclusion,
          enabled: true
        };

        const res = await ApiClient.createRule(newRule);
        showToast(res.message || "Tạo luật thành công", "success");
        closeModal();
        addForm.reset();
        await loadAdminDashboard();
      } catch (err) {
        showToast("Lỗi: " + err.message, "error");
      }
    });
  }
}
