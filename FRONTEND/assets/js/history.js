/**
 * HISTORY LOG CONTROLLER
 */

document.addEventListener("DOMContentLoaded", async () => {
  const historyList = await ApiClient.getHistory();
  renderHistoryTable(historyList);
  initClearHistory();
});

function renderHistoryTable(list) {
  const tbody = document.getElementById("historyTableBody");
  if (!tbody) return;

  if (!list || list.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7">
          <div class="empty-history-state">
            <i class="fas fa-history empty-icon"></i>
            <h3 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem;">Chưa có lịch sử tư vấn nào</h3>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1.5rem;">
              Hãy hoàn thành phiên tư vấn đầu tiên để hệ thống lưu trữ kết quả và biểu đồ của bạn.
            </p>
            <a href="consultation.html" class="btn btn-primary">
              <i class="fas fa-play"></i> Bắt đầu tư vấn ngay
            </a>
          </div>
        </td>
      </tr>
    `;
    return;
  }

  let html = "";
  list.forEach(item => {
    html += `
      <tr>
        <td><strong style="color: var(--primary-600);">${item.id}</strong></td>
        <td>${item.date}</td>
        <td><strong>${item.studentName}</strong></td>
        <td><span class="badge badge-purple">${item.hollandCode}</span></td>
        <td><strong>${item.targetCareer}</strong></td>
        <td><span class="badge badge-success">${item.matchRate}%</span></td>
        <td style="text-align: right;">
          <button class="btn btn-secondary btn-sm" onclick="viewHistoryDetail('${item.id}')">
            <i class="fas fa-eye"></i> Xem lại
          </button>
        </td>
      </tr>
    `;
  });

  tbody.innerHTML = html;
}

window.viewHistoryDetail = function(id) {
  const history = ApiClient.getHistorySync();
  const record = history.find(h => h.id === id);
  if (record && record.details) {
    sessionStorage.setItem("current_consultation_result", JSON.stringify(record.details));
    window.location.href = "result.html";
  } else {
    showToast("Không tìm thấy chi tiết phiên này", "error");
  }
};

function initClearHistory() {
  const btn = document.getElementById("btnClearHistory");
  if (!btn) return;

  btn.addEventListener("click", () => {
    if (confirm("Bạn có chắc chắn muốn xóa toàn bộ lịch sử tư vấn không?")) {
      localStorage.removeItem("career_consultation_history");
      renderHistoryTable([]);
      showToast("Đã dọn dẹp sạch lịch sử tư vấn", "success");
    }
  });
}
