# HỆ CHUYÊN GIA TƯ VẤN CHỌN NGÀNH/NGHỀ CHO HỌC SINH THPT (EduCareer AI)

> **Dự án Hệ Chuyên Gia (Rule-Based Expert System)** hỗ trợ học sinh THPT định hướng ngành nghề và chọn tổ hợp xét tuyển đại học tối ưu dựa trên **Mô hình tính cách John Holland (RIASEC)**, **Năng lực học bạ văn hóa**, và **Thuật toán Suy diễn tiến (Forward Chaining)** kết hợp cơ chế giải quyết xung đột tri thức.

---

## 📑 MỤC LỤC
1. [Giới thiệu tổng quan](#1-giới-thiệu-tổng-quan)
2. [Kiến trúc hệ thống](#2-kiến-trúc-hệ-thống)
3. [Cơ sở tri thức & Thuật toán suy diễn](#3-cơ-sở-tri-thức--thuật-toán-suy-diễn)
4. [Cấu trúc thư mục dự án](#4-cấu-trúc-thư-mục-dự-án)
5. [Công nghệ sử dụng](#5-công-nghệ-sử-dụng)
6. [Hướng dẫn cài đặt & Khởi chạy](#6-hướng-dẫn-cài-đặt--khởi-chạy)
7. [Tài liệu API RESTful](#7-tài-liệu-api-restful)
8. [Kiểm thử tự động (Testing)](#8-kiểm-thử-tự-động-testing)
9. [Phân công vai trò thành viên](#9-phân-công-vai-trò-thành-viên)

---

## 1. Giới thiệu tổng quan

Trước ngưỡng cửa kỳ thi tốt nghiệp THPT và xét tuyển đại học, học sinh thường gặp nhiều khó khăn trong việc lựa chọn ngành nghề phù hợp với năng lực và sở thích thực tế. **EduCareer AI** được xây dựng nhằm giải quyết bài toán đó thông qua:
- **Đánh giá đa chiều:** Kết hợp điểm trung bình 8 môn văn hóa (Toán, Lý, Hóa, Sinh, Văn, Anh, Tin, Sử/Địa) với bài trắc nghiệm tâm lý nghề nghiệp RIASEC 6 nhóm.
- **Suy diễn minh bạch (Explainable AI):** Không phải là mô hình hộp đen (Black-box), hệ thống ghi lại **Vết suy diễn (Explanation Trace)** cho biết chính xác luật nào đã được kích hoạt (*Fired Rules*), tại sao lại đề xuất ngành nghề đó.
- **Thực tế tuyển sinh:** Tích hợp dữ liệu tổ hợp xét tuyển (A00, A01, B00, C00, D01, H00, V00...), điểm chuẩn tham chiếu và danh sách các trường đại học đào tạo hàng đầu tại Việt Nam.

---

## 2. Kiến trúc hệ thống

Hệ thống được thiết kế theo cấu trúc chuẩn mực của một **Hệ Chuyên Gia Dựa Trên Luật (Production Rule Expert System)** gồm 4 thành phần cốt lõi:

```mermaid
flowchart TD
    subgraph UI [Giao diện Người dùng - Frontend]
        A[Học sinh THPT] -->|Nhập điểm, làm trắc nghiệm RIASEC| B[Consultation Wizard]
        B -->|Gửi Payload| C[API Client / Fallback Engine]
        D[Báo cáo Kết quả & Radar Chart] <-- C
    end

    subgraph Backend [Hệ thống Xử lý - Backend FastAPI]
        C -->|POST /api/consultations/evaluate| E[Consultation Service]
        
        subgraph ExpertCore [Lõi Hệ Chuyên Gia]
            F[1. Bộ chuyển đổi Fact Base] -->|Working Memory| G[3. Động cơ Suy diễn tiến]
            H[2. Knowledge Base - Tập luật IF-THEN] --> G
            G -->|Conflict Set| I[4. Bộ giải quyết Xung đột & Ranking]
            G -->|Execution Trace| J[5. Bộ giải thích Vết suy diễn]
        end
        
        E --> F
        I --> E
        J --> E
    end

    subgraph Data [Cơ sở Dữ liệu & Tri thức]
        K[(SQLite DB / JSON)] <--> E
        H <-->|Đọc 35+ Rules| L[rules.json & fact_conventions.json]
    end
```

1. **Bộ nhớ làm việc (Working Memory / Fact Base):** Lưu trữ tập sự kiện ban đầu của học sinh và các sự kiện trung gian sinh ra trong quá trình suy luận.
2. **Cơ sở tri thức (Knowledge Base):** Tập luật sản xuất 2 tầng (Tầng 1 suy diễn năng lực & sở thích; Tầng 2 suy diễn nhóm ngành nghề).
3. **Động cơ suy diễn (Inference Engine):** Triển khai thuật toán **Suy diễn tiến (Forward Chaining)** với cơ chế khúc xạ (*Refraction*) chống lặp vô hạn.
4. **Bộ phận giải thích (Explanation Facility):** Trích xuất lịch sử các bước kích hoạt luật, cung cấp căn cứ thuyết phục cho học sinh và phụ huynh.

---

## 3. Cơ sở tri thức & Thuật toán suy diễn

### 3.1. Cấu trúc luật IF-THEN
Mỗi luật trong `DATABASE/data/rules.json` có cấu trúc:
```json
{
  "id": "GRP-01",
  "name": "CNTT: logic cao + thích công nghệ",
  "description": "Toán & Tin học tốt kết hợp đam mê công nghệ là tiền đề vững chắc cho ngành Công nghệ thông tin.",
  "category": "career_group",
  "conditions": [
    {"attribute": "ability.logic", "operator": "==", "value": "high"},
    {"attribute": "interest.tech", "operator": "==", "value": "high"}
  ],
  "conclusion": {
    "type": "recommendation",
    "career_group": "CNTT",
    "careers": ["it_software", "ai_data"]
  },
  "priority": 9,
  "confidence": 0.95,
  "enabled": true
}
```

### 3.2. Hai loại kết luận (Conclusion)
- **`type: "fact"`:** Sinh ra Fact trung gian (dẫn xuất) bổ sung vào Working Memory (ví dụ: `ability.logic = "high"`, `interest.health = "high"`).
- **`type: "recommendation"`:** Đề xuất nhóm ngành và danh sách mã nghề tương ứng (`CNTT`, `YDUOC`, `KINHTE`, `NGHETHUAT`, `KYTHUAT`, `GIAODUC`).

### 3.3. Chiến lược giải quyết xung đột (Conflict Resolution)
Khi có nhiều luật cùng thỏa mãn điều kiện ở một chu kỳ suy diễn (*Conflict Set*):
1. **Độ tin cậy (`confidence`):** Luật có độ chắc chắn cao hơn (0.0 -> 1.0) được ưu tiên bắn trước.
2. **Độ ưu tiên (`priority`):** Tiêu chí phụ khi confidence bằng nhau (mức từ 1 đến 10).
3. **Độ cụ thể (`specificity`):** Luật có nhiều điều kiện ràng buộc hơn được ưu tiên so với luật tổng quát.
4. **Khúc xạ (`refraction`):** Mỗi luật chỉ được bắn tối đa 1 lần trong suốt phiên suy diễn.

---

## 4. Cấu trúc thư mục dự án

```text
EXPERT_SYSTEM_CAREER/
├── BACKEND/                         # Mã nguồn máy chủ Backend Python FastAPI
│   ├── app/
│   │   ├── api/                     # Router API: health, careers, consultation, history
│   │   ├── database/                # Kết nối SQLite, repositories (Career, Rule, Student, Consultation)
│   │   ├── expert_system/           # Lõi Hệ Chuyên Gia
│   │   │   ├── facts/               # Thành viên 1: Biểu diễn & kiểm tra Fact
│   │   │   ├── knowledge_base/      # Thành viên 2: Quản lý & kiểm tra luật
│   │   │   ├── inference/           # Thành viên 3: Động cơ suy diễn tiến
│   │   │   ├── conflict_resolution/ # Thành viên 4: Bộ giải quyết xung đột & Xếp hạng
│   │   │   └── explanation/         # Thành viên 5: Vết suy diễn & Giải thích
│   │   ├── models/                  # Data classes: Rule, Career, Student, Consultation
│   │   ├── schemas/                 # Pydantic schemas cho Request & Response
│   │   ├── services/                # Nghiệp vụ điều phối chính
│   │   └── utils/                   # Constants, Logger, HTTP Response Handler
│   ├── tests/                       # Bộ 158 test case tự động (pytest)
│   ├── config.py                    # Cấu hình môi trường, CORS, Port
│   └── run.py                       # Điểm khởi chạy Uvicorn Server
│
├── FRONTEND/                        # Giao diện Web Client
│   ├── index.html                   # Trang chủ điều hướng
│   ├── pages/
│   │   ├── home.html                # Trang chủ chi tiết
│   │   ├── consultation.html        # Form nhập liệu Stepper 4 bước & trắc nghiệm RIASEC
│   │   ├── result.html              # Bảng xếp hạng ngành, biểu đồ Radar Chart & Vết suy diễn
│   │   ├── career-list.html         # Tra cứu cơ sở tri thức ngành nghề & khối thi
│   │   ├── career-detail.html       # Chi tiết ngành học, mức lương, trường đào tạo
│   │   ├── history.html             # Lịch sử các lần tư vấn của học sinh
│   │   ├── about.html               # Tài liệu học thuật về kiến trúc hệ thống
│   │   └── 404.html                 # Trang báo lỗi đường dẫn
│   ├── components/                  # Header, Navbar, Footer, Sidebar, Cards, Loading modal
│   └── assets/
│       ├── css/                     # style.css, consultation.css, result.css, responsive.css
│       └── js/                      # api.js, consultation.js, result.js, validation.js, main.js
│
├── DATABASE/                        # Cơ sở dữ liệu & Tập luật
│   ├── data/
│   │   ├── rules.json               # 35+ luật sản xuất 2 tầng
│   │   ├── fact_conventions.json    # Quy ước tên thuộc tính & miền giá trị Fact
│   │   ├── career_details.json      # Dữ liệu chi tiết 8 ngành nghề trọng điểm
│   │   ├── career_categories.json   # Danh mục 6 khối ngành
│   │   └── admission_reference.csv  # Điểm chuẩn tham chiếu 2024-2025
│   ├── schema.sql                   # Cấu trúc bảng SQLite
│   └── seed.sql                     # Script nạp dữ liệu mẫu
│
├── DOCUMENTATION/                   # 14 tài liệu đặc tả kiến trúc & kỹ thuật
├── requirements.txt                 # Danh sách thư viện Python
├── .env.example                     # Mẫu biến môi trường
└── README.md                        # Hướng dẫn tổng thể của bài
```

---

## 5. Công nghệ sử dụng

| Tầng | Công nghệ / Thư viện | Vai trò |
|---|---|---|
| **Backend** | Python 3.10+, FastAPI, Uvicorn | Xây dựng RESTful API hiệu năng cao |
| **Expert Core** | Thuật toán Forward Chaining, Dataclasses | Động cơ suy diễn luật và giải quyết xung đột |
| **Validation** | Pydantic v2 | Kiểm tra kiểu dữ liệu đầu vào / đầu ra API |
| **Database** | SQLite3, JSON Data Store | Lưu trữ hồ sơ học sinh, luật và phiên tư vấn |
| **Frontend** | HTML5, CSS3 (Modern Responsive, Dark/Light Mode), Vanilla JavaScript | Giao diện thân thiện, mượt mà, không phụ thuộc nặng framework |
| **Visuals** | Chart.js, FontAwesome 6, Google Fonts | Biểu đồ Radar RIASEC, icon học đường |
| **Testing** | Pytest, FastAPI TestClient | 158 kiểm thử tự động đạt độ bao phủ toàn diện |

---

## 6. Hướng dẫn cài đặt & Khởi chạy

### 6.1. Yêu cầu môi trường
- **Python:** Phiên bản 3.10 trở lên.
- **Trình duyệt web:** Google Chrome, Microsoft Edge, Firefox, Cốc Cốc...

### 6.2. Cài đặt Backend
1. Mở terminal tại thư mục gốc dự án:
   ```bash
   cd d:\EXPERT_SYSTEM_CAREER
   ```
2. Cài đặt các gói phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```
3. Khởi chạy máy chủ Backend:
   ```bash
   python BACKEND/run.py
   ```
   *Máy chủ sẽ hoạt động tại:* `http://127.0.0.1:8000`  
   *Xem tài liệu API trực quan Swagger UI tại:* `http://127.0.0.1:8000/docs`

### 6.3. Khởi chạy Frontend
- Cách 1: Mở trực tiếp file [`FRONTEND/index.html`](file:///d:/EXPERT_SYSTEM_CAREER/FRONTEND/index.html) bằng bất kỳ trình duyệt nào.
- Cách 2: Sử dụng tiện ích **Live Server** của VS Code để khởi chạy tại cổng `http://127.0.0.1:5500`.

> **Lưu ý tính năng Fallback:** Trong trường hợp chưa bật Backend, Frontend tích hợp sẵn bộ máy suy diễn nội bộ `Client-Side Expert Engine` tại [`FRONTEND/assets/js/api.js`](file:///d:/EXPERT_SYSTEM_CAREER/FRONTEND/assets/js/api.js) giúp giao diện vẫn thực hiện suy diễn và hiển thị đầy đủ kết quả trắc nghiệm RIASEC ngay lập tức.

---

## 7. Tài liệu API RESTful

### 7.1. Đánh giá tư vấn (Consultation Evaluation)
- **Endpoint:** `POST /api/consultations/evaluate`
- **Payload mẫu:**
```json
{
  "student": {
    "fullName": "Nguyễn Văn A",
    "grade": "12",
    "school": "THPT Chuyên Lê Hồng Phong",
    "region": "south",
    "track": "khoa_hoc_tu_nhien"
  },
  "scores": {
    "math": 8.5,
    "physics": 8.0,
    "chemistry": 7.0,
    "biology": 6.5,
    "literature": 7.0,
    "english": 8.5,
    "informatics": 9.0,
    "history": 7.0
  },
  "riasec": {
    "R": 80,
    "I": 95,
    "A": 60,
    "S": 65,
    "E": 70,
    "C": 80
  },
  "preferences": {
    "environment": "tech",
    "tuition": "standard",
    "priority": "high_salary"
  }
}
```
- **Response:** Trả về `consultationId`, mã Holland `dominantCode`, danh sách xếp hạng ngành nghề kèm tỷ lệ % phù hợp và vết giải thích `explanationSummary`.

### 7.2. Các Endpoint khác
- `GET /api/health`: Kiểm tra trạng thái máy chủ.
- `GET /api/careers`: Lấy danh mục toàn bộ ngành nghề.
- `GET /api/careers/{career_id}`: Xem chi tiết một ngành học cụ thể.
- `GET /api/history`: Lấy danh sách lịch sử các phiên tư vấn.

---

## 8. Kiểm thử tự động (Testing)

Dự án trang bị bộ kiểm thử toàn diện với **158 test cases**, bao phủ toàn bộ các tầng logic từ đơn vị đến tích hợp:
- **`test_facts.py`:** Kiểm thử tạo và kiểm tra tính hợp lệ của thuộc tính Fact theo quy ước.
- **`test_knowledge_base.py`:** Kiểm thử nạp luật, cú pháp logic, validator, phát hiện luật trùng lặp.
- **`test_inference.py`:** Kiểm thử thuật toán suy diễn tiến, kiểm tra điều kiện (AND/OR/NOT), chuỗi suy luận nhiều bước (*multi-step chaining*), cơ chế dừng fixed point.
- **`test_conflict_resolution.py`:** Kiểm thử phát hiện và giải quyết xung đột luật theo độ tin cậy và xếp hạng.
- **`test_explanation.py`:** Kiểm thử trích xuất vết suy diễn và sinh văn bản giải thích.
- **`test_consultation_api.py`:** Kiểm thử các endpoint API thông qua FastAPI TestClient.
- **`test_integration.py`:** Kiểm thử toàn trình luồng End-to-End từ hồ sơ học sinh đến kết quả đề xuất cuối cùng.

**Lệnh chạy kiểm thử:**
```bash
pytest BACKEND/tests -v
```
*(Kết quả: 158 passed in 0.60s)*

---

## 9. Phân công vai trò thành viên

Dự án được phân bổ khoa học theo 5 vai trò thành viên chuyên trách:

| Thành viên | Trách nhiệm chính | Mô-đun phụ trách |
|---|---|---|
| **Thành viên 1** | Quản lý & Mô hình hóa Sự kiện (Facts) | `app/expert_system/facts/`, `DATABASE/data/fact_conventions.json` |
| **Thành viên 2** | Cơ sở tri thức & Quản lý tập luật (Knowledge Base) | `app/expert_system/knowledge_base/`, `DATABASE/data/rules.json` |
| **Thành viên 3** | Động cơ suy diễn tiến (Inference Engine) | `app/expert_system/inference/` |
| **Thành viên 4** | Phát hiện xung đột & Thuật toán Xếp hạng | `app/expert_system/conflict_resolution/` |
| **Thành viên 5** | Bộ giải thích vết suy diễn (Explanation Facility) | `app/expert_system/explanation/` |
| **Tích hợp** | Thiết kế giao diện Frontend & Tích hợp API FastAPI | `FRONTEND/`, `BACKEND/app/api/`, `BACKEND/app/services/` |

---

© 2026 **EduCareer AI Team**. Mã nguồn mở phục vụ mục đích nghiên cứu và giáo dục định hướng nghề nghiệp THPT.
