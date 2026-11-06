/**
 * RESULT PAGE CONTROLLER
 * Render danh sách ngành được gợi ý, radar chart RIASEC và vết suy diễn giải thích
 */

document.addEventListener("DOMContentLoaded", () => {
  loadAndRenderResult();
  initPrintBtn();
});

function loadAndRenderResult() {
  // Đọc từ sessionStorage, nếu chưa có thì lấy bản ghi mới nhất từ history hoặc mẫu mặc định
  let resultData = null;
  const sessionData = sessionStorage.getItem("current_consultation_result");
  
  if (sessionData) {
    try {
      resultData = JSON.parse(sessionData);
    } catch(e) {
      console.error(e);
    }
  }

  // Dữ liệu mẫu nếu học sinh vào thẳng trang result.html
  if (!resultData) {
    const historyList = ApiClient.getHistorySync();
    if (historyList.length > 0 && historyList[0].details) {
      resultData = historyList[0].details;
    } else {
      // Chạy một lượt mẫu
      resultData = ExpertInferenceEngine.infer({
        student: { fullName: "Nguyễn Minh Quân", grade: "12", school: "THPT Chuyên Lê Hồng Phong" },
        scores: { math: 9.0, physics: 8.5, chemistry: 7.5, biology: 7.0, literature: 7.5, english: 8.5, informatics: 9.5, history: 6.5 },
        riasec: { R: 80, I: 100, A: 60, S: 70, E: 65, C: 85 },
        preferences: { environment: "tech", tuition: "standard", priority: "high_salary" }
      });
    }
  }

  // 1. Render Student Metadata
  renderMetaBadges(resultData);

  // 2. Render Cards
  renderRecommendationCards(resultData.recommendations);

  // 3. Render Radar Chart
  renderRadarChart(resultData.riasecScores);

  // 4. Render Recommended Exam Blocks
  renderExamBlocks(resultData.recommendations);
}

function renderMetaBadges(data) {
  const metaContainer = document.getElementById("studentMetaBadges");
  if (!metaContainer) return;

  metaContainer.innerHTML = `
    <span class="meta-tag"><i class="fas fa-user-graduate"></i> Học sinh: <strong>${data.student.fullName} (Lớp ${data.student.grade})</strong></span>
    <span class="meta-tag"><i class="fas fa-school"></i> ${data.student.school || "THPT"}</span>
    <span class="meta-tag"><i class="fas fa-fingerprint"></i> Mã Holland: <strong>${data.dominantCode}</strong></span>
    <span class="meta-tag"><i class="fas fa-calendar-alt"></i> ${new Date().toLocaleDateString("vi-VN")}</span>
  `;
}

function renderRecommendationCards(recommendations) {
  const container = document.getElementById("recommendationsContainer");
  if (!container) return;

  let html = "";
  recommendations.slice(0, 5).forEach((item, index) => {
    const rank = index + 1;
    const isTop = rank === 1;
    const badgeClass = isTop ? "badge-success" : (rank === 2 ? "badge-primary" : "badge-warning");
    const rankText = `TOP ${rank} PHÙ HỢP`;

    const rulesHtml = item.rulesFired.map(r => `<li><i class="fas fa-check" style="color:var(--accent-emerald); margin-right:4px;"></i> ${r}</li>`).join("");

    html += `
      <div class="career-match-card ${isTop ? 'rank-top' : ''}">
        <div class="rank-badge-ribbon">
          <span class="badge ${badgeClass}">${rankText}</span>
        </div>

        <div class="match-header">
          <div>
            <span class="badge badge-primary" style="margin-bottom: 0.5rem;">${item.career.category}</span>
            <h3 class="career-name">${item.career.name}</h3>
            <p class="career-cat"><i class="fas fa-barcode"></i> Mã xét tuyển: ${item.career.code} | Khối: ${item.career.required_blocks.join(", ")}</p>
          </div>

          <div class="match-score-radial">
            <span class="number">${item.matchScore}</span>
            <span class="unit">%</span>
          </div>
        </div>

        <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1rem; line-height: 1.6;">
          ${item.career.description}
        </p>

        <div class="score-breakdown-grid">
          <div class="breakdown-item">
            <p>Học lực môn thi: <strong>${item.academicMatch}%</strong></p>
            <div class="progress-bar-custom">
              <div class="progress-fill" style="width: ${item.academicMatch}%;"></div>
            </div>
          </div>
          <div class="breakdown-item">
            <p>Tính cách RIASEC: <strong>${item.personalityMatch}%</strong></p>
            <div class="progress-bar-custom">
              <div class="progress-fill" style="width: ${item.personalityMatch}%; background: var(--secondary-500);"></div>
            </div>
          </div>
          <div class="breakdown-item">
            <p>Tiềm năng thị trường: <strong>${item.marketMatch}%</strong></p>
            <div class="progress-bar-custom">
              <div class="progress-fill" style="width: ${item.marketMatch}%; background: var(--accent-emerald);"></div>
            </div>
          </div>
        </div>

        <div class="expert-explanation-box">
          <h5>
            <i class="fas fa-microchip"></i>
            Vết suy diễn chuyên gia (Explanation Trace):
          </h5>
          <ul class="rules-fired-list">
            ${rulesHtml || "<li>Áp dụng luật suy luận tương thích tổ hợp điểm khối A00/A01.</li>"}
          </ul>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1.5rem; flex-wrap: wrap; gap: 1rem;">
          <div>
            <span style="font-size: 0.85rem; color: var(--text-muted);">Trường đại học đào tạo tiêu biểu: </span>
            <strong style="font-size: 0.88rem; color: var(--text-main);">${item.career.top_universities.join(", ")}</strong>
          </div>
          <a href="career-detail.html?id=${item.career.id}" class="btn btn-outline btn-sm">
            <i class="fas fa-info-circle"></i> Xem lộ trình học
          </a>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function renderRadarChart(scores) {
  const canvas = document.getElementById("riasecRadarChart");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const data = [
    scores.R || 50,
    scores.I || 50,
    scores.A || 50,
    scores.S || 50,
    scores.E || 50,
    scores.C || 50
  ];

  new Chart(ctx, {
    type: "radar",
    data: {
      labels: ["R - Thực tế", "I - Nghiên cứu", "A - Nghệ thuật", "S - Xã hội", "E - Quản lý", "C - Nghiệp vụ"],
      datasets: [{
        label: "Điểm RIASEC (%)",
        data: data,
        backgroundColor: "rgba(37, 99, 235, 0.25)",
        borderColor: "#2563eb",
        pointBackgroundColor: "#7c3aed",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "#2563eb",
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { color: "rgba(148, 163, 184, 0.3)" },
          grid: { color: "rgba(148, 163, 184, 0.2)" },
          suggestedMin: 0,
          suggestedMax: 100,
          ticks: { stepSize: 20, display: false }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

function renderExamBlocks(recommendations) {
  const container = document.getElementById("recommendedBlocksContainer");
  if (!container) return;

  const blocksSet = new Set();
  recommendations.slice(0, 3).forEach(r => {
    r.career.required_blocks.forEach(b => blocksSet.add(b));
  });

  let html = "";
  blocksSet.forEach(b => {
    html += `<span class="block-tag"><i class="fas fa-graduation-cap"></i> ${b}</span>`;
  });
  container.innerHTML = html;
}

function initPrintBtn() {
  const printBtn = document.getElementById("btnPrintReport");
  if (printBtn) {
    printBtn.addEventListener("click", () => {
      window.print();
    });
  }
}
