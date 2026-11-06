/**
 * CONSULTATION WIZARD CONTROLLER
 * Điều phối Stepper 4 bước, cập nhật slider điểm số, RIASEC và kích hoạt Expert Engine
 */

document.addEventListener("DOMContentLoaded", () => {
  initStepper();
  initScoreSliders();
  initRiasecRadios();
  initSelectCards();
  initConsultationSubmission();
});

// Stepper controller
function initStepper() {
  const stepItems = document.querySelectorAll(".step-item");
  const stepPanes = document.querySelectorAll(".form-step-pane");
  const progressBar = document.getElementById("stepperProgressBar");

  function goToStep(stepNumber) {
    // Cập nhật classes cho Stepper navigation
    stepItems.forEach(item => {
      const step = parseInt(item.dataset.step);
      item.classList.remove("active");
      if (step === stepNumber) {
        item.classList.add("active");
      } else if (step < stepNumber) {
        item.classList.add("completed");
      } else {
        item.classList.remove("completed");
      }
    });

    // Cập nhật thanh tiến độ %
    const progressPercent = ((stepNumber - 1) / (stepItems.length - 1)) * 100;
    if (progressBar) progressBar.style.width = `${progressPercent}%`;

    // Hiển thị Pane tương ứng
    stepPanes.forEach((pane, idx) => {
      if (idx + 1 === stepNumber) {
        pane.classList.add("active");
      } else {
        pane.classList.remove("active");
      }
    });

    window.scrollTo({ top: 120, behavior: "smooth" });
  }

  // Nút Tiếp tục
  document.querySelectorAll(".btn-next-step").forEach(btn => {
    btn.addEventListener("click", () => {
      const targetStep = parseInt(btn.dataset.target);
      
      // Kiểm tra validate nếu từ bước 1 sang bước 2
      if (targetStep === 2) {
        const form1 = document.getElementById("stepPane1");
        if (!Validator.validateStudentStep(form1)) {
          showToast("Vui lòng điền đầy đủ họ tên và chọn khối lớp của học sinh!", "warning");
          return;
        }
      }

      goToStep(targetStep);
    });
  });

  // Nút Quay lại
  document.querySelectorAll(".btn-prev-step").forEach(btn => {
    btn.addEventListener("click", () => {
      const targetStep = parseInt(btn.dataset.target);
      goToStep(targetStep);
    });
  });

  // Cho phép bấm trực tiếp vào các bước đã hoàn thành
  stepItems.forEach(item => {
    item.addEventListener("click", () => {
      const step = parseInt(item.dataset.step);
      goToStep(step);
    });
  });
}

// Cập nhật nhãn hiển thị điểm số khi kéo slider
function initScoreSliders() {
  const subjects = [
    { slider: "scoreMath", display: "displayScoreMath" },
    { slider: "scorePhysics", display: "displayScorePhysics" },
    { slider: "scoreChemistry", display: "displayScoreChemistry" },
    { slider: "scoreBiology", display: "displayScoreBiology" },
    { slider: "scoreLiterature", display: "displayScoreLiterature" },
    { slider: "scoreEnglish", display: "displayScoreEnglish" },
    { slider: "scoreInformatics", display: "displayScoreInformatics" },
    { slider: "scoreHistory", display: "displayScoreHistory" }
  ];

  subjects.forEach(sub => {
    const sliderEl = document.getElementById(sub.slider);
    const displayEl = document.getElementById(sub.display);
    if (sliderEl && displayEl) {
      sliderEl.addEventListener("input", (e) => {
        displayEl.textContent = parseFloat(e.target.value).toFixed(1);
      });
    }
  });
}

// Tương tác bảng đánh giá RIASEC
function initRiasecRadios() {
  const questionRows = document.querySelectorAll(".riasec-question-item");
  questionRows.forEach(row => {
    const pills = row.querySelectorAll(".rating-pill");
    pills.forEach(pill => {
      pill.addEventListener("click", () => {
        pills.forEach(p => p.classList.remove("selected"));
        pill.classList.add("selected");
      });
    });
  });
}

// Selectable card UI
function initSelectCards() {
  document.querySelectorAll(".select-card-option").forEach(card => {
    card.addEventListener("click", () => {
      const radio = card.querySelector("input[type='radio']");
      if (radio) {
        const name = radio.getAttribute("name");
        document.querySelectorAll(`input[name="${name}"]`).forEach(r => {
          r.closest(".select-card-option").classList.remove("checked");
        });
        radio.checked = true;
        card.classList.add("checked");
      }
    });
  });
}

// Gửi toàn bộ dữ liệu & chạy Engine
function initConsultationSubmission() {
  const submitBtn = document.getElementById("btnSubmitConsultation");
  if (!submitBtn) return;

  submitBtn.addEventListener("click", async () => {
    // 1. Thu thập thông tin học sinh
    const student = {
      fullName: document.getElementById("studentName").value.trim() || "Học sinh THPT",
      grade: document.getElementById("studentGrade").value || "12",
      school: document.getElementById("studentSchool").value.trim() || "Chưa xác định",
      region: document.getElementById("studentRegion").value || "south",
      track: document.querySelector('input[name="mainComboTrack"]:checked')?.value || "khoa_hoc_tu_nhien"
    };

    // 2. Thu thập điểm học tập
    const scores = {
      math: parseFloat(document.getElementById("scoreMath").value) || 8.0,
      physics: parseFloat(document.getElementById("scorePhysics").value) || 8.0,
      chemistry: parseFloat(document.getElementById("scoreChemistry").value) || 7.0,
      biology: parseFloat(document.getElementById("scoreBiology").value) || 7.0,
      literature: parseFloat(document.getElementById("scoreLiterature").value) || 7.5,
      english: parseFloat(document.getElementById("scoreEnglish").value) || 8.5,
      informatics: parseFloat(document.getElementById("scoreInformatics").value) || 9.0,
      history: parseFloat(document.getElementById("scoreHistory").value) || 7.0
    };

    // 3. Thu thập điểm RIASEC
    const riasec = {};
    document.querySelectorAll(".riasec-question-item").forEach(item => {
      const type = item.dataset.type;
      const selectedPill = item.querySelector(".rating-pill.selected");
      riasec[type] = selectedPill ? parseInt(selectedPill.dataset.score) : 60;
    });

    // 4. Thu thập nguyện vọng
    const preferences = {
      environment: document.querySelector('input[name="prefEnvironment"]:checked')?.value || "tech",
      tuition: document.getElementById("prefTuition").value,
      priority: document.getElementById("prefPriority").value
    };

    const payload = { student, scores, riasec, preferences };

    // Hiển thị modal suy diễn
    showLoadingModal();

    // Mô phỏng các giai đoạn suy diễn của hệ chuyên gia
    await simulateInferenceSteps();

    // Gửi dữ liệu tính toán
    const result = await ApiClient.submitConsultation(payload);

    // Lưu phiên làm việc hiện tại vào sessionStorage để trang result.html đọc
    sessionStorage.setItem("current_consultation_result", JSON.stringify(result));

    // Chuyển hướng tới trang kết quả
    window.location.href = "result.html";
  });
}

function showLoadingModal() {
  const modal = document.getElementById("expertLoadingModal");
  if (modal) modal.style.display = "flex";
}

function simulateInferenceSteps() {
  return new Promise(resolve => {
    const statusText = document.getElementById("loadingStatusText");
    const progress = document.getElementById("loadingProgressLine");

    setTimeout(() => {
      if (statusText) statusText.textContent = "Bước 1/3: Chuẩn hóa véc-tơ học bạ & tính toán tổ hợp môn...";
      if (progress) progress.style.width = "50%";
    }, 400);

    setTimeout(() => {
      if (statusText) statusText.textContent = "Bước 2/3: Khớp tập luật IF-THEN RIASEC & kiểm tra tiền đề...";
      if (progress) progress.style.width = "75%";
    }, 850);

    setTimeout(() => {
      if (statusText) statusText.textContent = "Bước 3/3: Kích hoạt luật giải quyết xung đột & sinh vết giải thích...";
      if (progress) progress.style.width = "100%";
    }, 1300);

    setTimeout(resolve, 1700);
  });
}
