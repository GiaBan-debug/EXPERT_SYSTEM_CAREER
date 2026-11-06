/**
 * CAREER DATA & EXPERT SYSTEM MOCK ENGINE
 * Dùng làm nguồn dữ liệu chuẩn cho Frontend & dự phòng khi Backend chưa khởi chạy
 */

const CAREER_DATABASE = [
  {
    id: "it_software",
    code: "CNTT01",
    name: "Kỹ thuật Phần mềm / Lập trình viên",
    category: "Công nghệ Thông tin",
    icon: "fa-laptop-code",
    riasec_primary: "I",
    riasec_code: "IRC",
    description: "Thiết kế, xây dựng, tối ưu hóa và bảo trì các hệ thống ứng dụng phần mềm, web, ứng dụng di động và trí tuệ nhân tạo.",
    required_blocks: ["A00 (Toán - Lý - Hóa)", "A01 (Toán - Lý - Anh)"],
    top_universities: ["ĐH Bách Khoa", "ĐH Công nghệ - ĐHQG", "ĐH FPT", "Học viện CNBCVT"],
    average_salary: "15,000,000 - 40,000,000 VNĐ",
    market_trend: "Tăng trưởng rất cao",
    weights: {
      math: 0.3,
      physics: 0.2,
      english: 0.2,
      riasec_I: 0.2,
      logic_preference: 0.1
    },
    rules: [
      "NẾU điểm Toán >= 7.5 VÀ RIASEC(I) >= 60% THÌ độ phù hợp Kỹ thuật phần mềm tăng mạnh",
      "NẾU thích làm việc với máy tính & công nghệ mới THÌ khuyến nghị nhóm ngành CNTT",
      "NẾU định hướng khối A00 hoặc A01 THÌ tỷ lệ trúng tuyển cao"
    ]
  },
  {
    id: "ai_data",
    code: "CNTT02",
    name: "Khoa học Dữ liệu & Trí tuệ Nhân tạo (AI)",
    category: "Công nghệ Thông tin",
    icon: "fa-brain",
    riasec_primary: "I",
    riasec_code: "IRC",
    description: "Nghiên cứu mô hình học máy, phân tích dữ liệu lớn và kiến tạo các giải pháp tự động hóa thông minh.",
    required_blocks: ["A00 (Toán - Lý - Hóa)", "A01 (Toán - Lý - Anh)"],
    top_universities: ["ĐH Bách Khoa", "ĐH Khoa học Tự nhiên", "VinUni"],
    average_salary: "20,000,000 - 55,000,000 VNĐ",
    market_trend: "Bùng nổ toàn cầu",
    weights: {
      math: 0.35,
      english: 0.25,
      riasec_I: 0.25,
      research_interest: 0.15
    },
    rules: [
      "NẾU Toán >= 8.0 VÀ điểm tư duy logic cao THÌ định hướng AI/Data Science",
      "NẾU tính cách thuộc nhóm Nghiên cứu (Investigative) THÌ rất phù hợp"
    ]
  },
  {
    id: "medical_doctor",
    code: "Y01",
    name: "Bác sĩ Đa khoa / Y khoa",
    category: "Y Dược & Chăm sóc Sức khỏe",
    icon: "fa-user-md",
    riasec_primary: "I",
    riasec_code: "ISR",
    description: "Khám chữa bệnh, tư vấn phòng ngừa và chăm sóc sức khỏe cho người bệnh trong hệ thống y tế công lập và tư nhân.",
    required_blocks: ["B00 (Toán - Hóa - Sinh)"],
    top_universities: ["ĐH Y Hà Nội", "ĐH Y Dược TP.HCM", "Học viện Quân Y"],
    average_salary: "15,000,000 - 35,000,000+ VNĐ",
    market_trend: "Nhu cầu bền vững, luôn cấp thiết",
    weights: {
      biology: 0.3,
      chemistry: 0.3,
      math: 0.15,
      riasec_S: 0.15,
      social_interest: 0.1
    },
    rules: [
      "NẾU Hóa >= 8.0 VÀ Sinh >= 8.0 VÀ RIASEC(S) >= 60% THÌ đề xuất nhóm ngành Y Dược",
      "NẾU mong muốn giúp đỡ cộng đồng và chịu được áp lực ca trực THÌ ưu tiên Y Đa khoa"
    ]
  },
  {
    id: "digital_marketing",
    code: "KT01",
    name: "Digital Marketing & Truyền thông Số",
    category: "Kinh tế & Marketing",
    icon: "fa-bullhorn",
    riasec_primary: "E",
    riasec_code: "EAS",
    description: "Xây dựng chiến dịch quảng bá, phát triển thương hiệu đa kênh và phân tích hành vi khách hàng trên không gian số.",
    required_blocks: ["D01 (Toán - Văn - Anh)", "A01 (Toán - Lý - Anh)"],
    top_universities: ["ĐH Ngoại thương", "ĐH Kinh tế Quốc dân", "ĐH Thương mại", "RMIT"],
    average_salary: "12,000,000 - 30,000,000 VNĐ",
    market_trend: "Tăng trưởng đều",
    weights: {
      literature: 0.25,
      english: 0.25,
      math: 0.15,
      riasec_E: 0.2,
      riasec_A: 0.15
    },
    rules: [
      "NẾU RIASEC(E) cao VÀ RIASEC(A) cao THÌ đề xuất Marketing/Truyền thông",
      "NẾU Văn >= 7.0 VÀ Tiếng Anh >= 7.5 THÌ phù hợp môi trường truyền thông sáng tạo"
    ]
  },
  {
    id: "graphic_design",
    code: "TK01",
    name: "Thiết kế Đồ họa & Mỹ thuật Đa phương tiện",
    category: "Nghệ thuật & Sáng tạo",
    icon: "fa-palette",
    riasec_primary: "A",
    riasec_code: "ARE",
    description: "Sáng tạo ấn phẩm hình ảnh, giao diện UI/UX người dùng, dựng hình 3D và truyền thông thị giác.",
    required_blocks: ["H00 (Văn - Năng khiếu)", "V00 (Toán - Lý - Vẽ)", "D01"],
    top_universities: ["ĐH Mỹ thuật Công nghiệp", "ĐH Kiến trúc", "Arena Multimedia"],
    average_salary: "10,000,000 - 28,000,000 VNĐ",
    market_trend: "Cao trong kỷ nguyên số",
    weights: {
      riasec_A: 0.4,
      literature: 0.2,
      english: 0.2,
      creative_preference: 0.2
    },
    rules: [
      "NẾU RIASEC(A) >= 70% THÌ kích hoạt nhóm ngành Thiết kế - Nghệ thuật",
      "NẾU yêu thích mỹ thuật và tư duy không gian tốt THÌ chọn Thiết kế Đồ họa"
    ]
  },
  {
    id: "logistics_supply",
    code: "KT02",
    name: "Logistics & Quản lý Chuỗi cung ứng",
    category: "Kinh tế & Quản lý",
    icon: "fa-dolly",
    riasec_primary: "C",
    riasec_code: "CEI",
    description: "Quản trị dòng vận chuyển nguyên vật liệu, tối ưu hóa kho bãi và mạng lưới phân phối thương mại quốc tế.",
    required_blocks: ["A01 (Toán - Lý - Anh)", "D01 (Toán - Văn - Anh)"],
    top_universities: ["ĐH Giao thông Vận tải", "ĐH Kinh tế Quốc dân", "ĐH Hàng hải"],
    average_salary: "12,000,000 - 32,000,000 VNĐ",
    market_trend: "Rất tiềm năng tại VN",
    weights: {
      math: 0.25,
      english: 0.3,
      riasec_C: 0.25,
      riasec_E: 0.2
    },
    rules: [
      "NẾU cẩn thận, quản lý logic quy trình tốt VÀ RIASEC(C) cao THÌ chọn Logistics"
    ]
  },
  {
    id: "automation_eng",
    code: "KT03",
    name: "Kỹ thuật Điều khiển & Tự động hóa / Robot",
    category: "Kỹ thuật & Công nghệ",
    icon: "fa-robot",
    riasec_primary: "R",
    riasec_code: "RIE",
    description: "Thiết kế, chế tạo dây chuyền tự động, lập trình tay máy robot và hệ thống cảm biến thông minh trong công nghiệp 4.0.",
    required_blocks: ["A00 (Toán - Lý - Hóa)", "A01 (Toán - Lý - Anh)"],
    top_universities: ["ĐH Bách Khoa", "ĐH Sư phạm Kỹ thuật", "ĐH Công nghiệp"],
    average_salary: "14,000,000 - 35,000,000 VNĐ",
    market_trend: "Tăng trưởng cao",
    weights: {
      math: 0.3,
      physics: 0.3,
      riasec_R: 0.25,
      riasec_I: 0.15
    },
    rules: [
      "NẾU Toán >= 7.5, Lý >= 8.0 VÀ RIASEC(R) cao THÌ định hướng Kỹ thuật Điều khiển & Tự động hóa"
    ]
  },
  {
    id: "pedagogy_edu",
    code: "SP01",
    name: "Sư phạm & Quản lý Giáo dục",
    category: "Giáo dục & Xã hội",
    icon: "fa-chalkboard-teacher",
    riasec_primary: "S",
    riasec_code: "SAI",
    description: "Giảng dạy, truyền đạt tri thức, nghiên cứu phương pháp giáo dục hiện đại và phát triển con người.",
    required_blocks: ["C00 (Văn - Sử - Địa)", "D01", "A00/B00 tuỳ môn"],
    top_universities: ["ĐH Sư phạm Hà Nội", "ĐH Sư phạm TP.HCM"],
    average_salary: "8,000,000 - 22,000,000 VNĐ",
    market_trend: "Chính sách học bổng & hỗ trợ cao",
    weights: {
      literature: 0.3,
      riasec_S: 0.4,
      communication_skill: 0.3
    },
    rules: [
      "NẾU RIASEC(S) >= 70% VÀ yêu thích giảng dạy, truyền đạt THÌ chọn Sư phạm"
    ]
  }
];

const API_BASE = "http://127.0.0.1:8000/api";

const ApiClient = {
  // Lấy danh sách ngành nghề
  async getCareers() {
    try {
      const res = await fetch(`${API_BASE}/careers`);
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn("Backend not running, using Local Database fallback.", e);
    }
    return CAREER_DATABASE;
  },

  // Chi tiết một ngành nghề
  async getCareerById(id) {
    try {
      const res = await fetch(`${API_BASE}/careers/${id}`);
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn("Using fallback career details.");
    }
    return CAREER_DATABASE.find(c => c.id === id) || CAREER_DATABASE[0];
  },

  // Gửi thông tin tư vấn lên Expert System Backend
  async submitConsultation(payload) {
    try {
      const res = await fetch(`${API_BASE}/consultations/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn("Backend API not reachable. Running Client-Side Expert Engine.");
    }
    // Chạy bộ suy diễn nội bộ nếu chưa có backend
    return ExpertInferenceEngine.infer(payload);
  },

  // Lấy lịch sử tư vấn
  async getHistory() {
    const local = localStorage.getItem("career_consultation_history");
    return local ? JSON.parse(local) : [];
  },

  saveHistory(item) {
    const list = this.getHistorySync();
    list.unshift(item);
    localStorage.setItem("career_consultation_history", JSON.stringify(list.slice(0, 30)));
  },

  getHistorySync() {
    const local = localStorage.getItem("career_consultation_history");
    return local ? JSON.parse(local) : [];
  }
};

/**
 * THUẬT TOÁN SUY DIỄN TIẾN (FORWARD CHAINING) TẠI CLIENT
 * Mô phỏng chính xác logic của Hệ Chuyên Gia
 */
const ExpertInferenceEngine = {
  infer(data) {
    const { student, scores, riasec, preferences } = data;
    
    // 1. Tính toán điểm chuẩn hóa các môn học (0 -> 100)
    const academicScores = {
      math: (parseFloat(scores.math) || 5) * 10,
      physics: (parseFloat(scores.physics) || 5) * 10,
      chemistry: (parseFloat(scores.chemistry) || 5) * 10,
      biology: (parseFloat(scores.biology) || 5) * 10,
      literature: (parseFloat(scores.literature) || 5) * 10,
      english: (parseFloat(scores.english) || 5) * 10,
      history: (parseFloat(scores.history) || 5) * 10,
      informatics: (parseFloat(scores.informatics) || 5) * 10
    };

    // 2. Tính điểm RIASEC (R, I, A, S, E, C)
    const riasecScores = {
      R: parseInt(riasec.R) || 30,
      I: parseInt(riasec.I) || 30,
      A: parseInt(riasec.A) || 30,
      S: parseInt(riasec.S) || 30,
      E: parseInt(riasec.E) || 30,
      C: parseInt(riasec.C) || 30
    };

    // Tìm Top 3 Holland Code
    const sortedRiasec = Object.entries(riasecScores).sort((a,b) => b[1] - a[1]);
    const dominantCode = sortedRiasec.slice(0, 3).map(x => x[0]).join("");

    // 3. Tiến hành suy diễn trên từng ngành trong tập luật
    const evaluatedResults = CAREER_DATABASE.map(career => {
      let matchScore = 45; // Điểm nền tảng
      const rulesFired = [];

      // Luật kiểm tra nhóm RIASEC chính
      if (career.riasec_primary === dominantCode[0]) {
        matchScore += 24;
        rulesFired.push(`LUẬT [R-01]: Nhóm tính cách chủ đạo (${dominantCode[0]}) hoàn toàn khớp với đặc thù ngành (${career.riasec_primary}).`);
      } else if (dominantCode.includes(career.riasec_primary)) {
        matchScore += 14;
        rulesFired.push(`LUẬT [R-02]: Tính cách (${dominantCode}) có giao thoa với mã ngành nghề.`);
      }

      // Luật kiểm tra học lực chuyên môn
      if (career.id.startsWith("it_")) {
        if (academicScores.math >= 80 && academicScores.english >= 70) {
          matchScore += 18;
          rulesFired.push("LUẬT [ACAD-IT]: Điểm Toán >= 8.0 & Ngoại ngữ đạt chuẩn tư duy thuật toán cao.");
        }
        if (preferences.environment === "tech") {
          matchScore += 10;
          rulesFired.push("LUẬT [PREF]: Học sinh chọn nguyện vọng ưu tiên thiết bị công nghệ & lập trình.");
        }
      } else if (career.id === "medical_doctor") {
        if (academicScores.biology >= 80 && academicScores.chemistry >= 80) {
          matchScore += 22;
          rulesFired.push("LUẬT [ACAD-MED]: Học lực Sinh học & Hóa học vượt trội (>= 8.0), đạt tiêu chí Y Dược.");
        }
      } else if (career.id === "graphic_design") {
        if (riasecScores.A >= 70) {
          matchScore += 20;
          rulesFired.push("LUẬT [ART-01]: Chỉ số sáng tạo nghệ thuật RIASEC(A) đạt ngưỡng cao (> 70%).");
        }
      } else if (career.id === "digital_marketing") {
        if (riasecScores.E >= 65 && academicScores.literature >= 70) {
          matchScore += 16;
          rulesFired.push("LUẬT [MKT-01]: Nhóm Quản trị/Thuyết phục (E) và năng lực Ngôn ngữ phù hợp.");
        }
      }

      // Giới hạn max score 98%
      matchScore = Math.min(Math.round(matchScore), 98);

      return {
        career,
        matchScore,
        academicMatch: Math.min(Math.round(matchScore * 0.95), 100),
        personalityMatch: Math.min(Math.round(riasecScores[career.riasec_primary] * 1.1), 100),
        marketMatch: 92,
        rulesFired
      };
    });

    // Sắp xếp kết quả theo độ phù hợp giảm dần
    evaluatedResults.sort((a,b) => b.matchScore - a.matchScore);

    const resultPayload = {
      consultationId: "CONS-" + Date.now().toString(36).toUpperCase(),
      createdAt: new Date().toISOString(),
      student,
      dominantCode,
      riasecScores,
      academicScores,
      recommendations: evaluatedResults
    };

    // Tự động lưu vào lịch sử
    ApiClient.saveHistory({
      id: resultPayload.consultationId,
      date: new Date().toLocaleDateString("vi-VN"),
      studentName: student.fullName,
      targetCareer: evaluatedResults[0].career.name,
      matchRate: evaluatedResults[0].matchScore,
      hollandCode: dominantCode,
      details: resultPayload
    });

    return resultPayload;
  }
};
