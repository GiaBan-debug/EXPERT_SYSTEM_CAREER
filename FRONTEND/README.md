# EduCareer AI - Giao Diện Frontend Hệ Chuyên Gia Tư Vấn Chọn Ngành/Nghề THPT

Bộ giao diện Frontend chuyên nghiệp, hiện đại và chuẩn mực dành cho bài toán **Hệ Chuyên Gia Tư Vấn Chọn Ngành/Nghề Cho Học Sinh THPT** dựa trên **Lý thuyết RIASEC John Holland** và **Thuật toán Suy diễn tiến (Forward Chaining)**.

---

## 📁 Cấu Trúc File & Thư Mục

```text
Frontend/
├── index.html                   # Trang chủ điều hướng chính của hệ thống
├── README.md                    # Tài liệu hướng dẫn sử dụng và triển khai
├── assets/
│   ├── css/
│   │   ├── style.css            # Biến màu, typography, CSS reset, header/footer, button, card
│   │   ├── home.css             # Giao diện Hero banner, quy trình 4 bước, 6 nhóm RIASEC
│   │   ├── consultation.css     # Form tư vấn dạng Stepper 4 bước, thanh trượt điểm số, radio RIASEC
│   │   ├── result.css           # Bảng xếp hạng ngành phù hợp, biểu đồ radar, vết suy diễn logic
│   │   ├── career.css           # Thẻ ngành nghề, bộ lọc tìm kiếm, trang chi tiết chuyên ngành
│   │   ├── history.css          # Bảng theo dõi nhật ký các lần tư vấn của học sinh
│   │   └── responsive.css       # Tương thích máy tính để bàn, iPad, Mobile màn hình nhỏ
│   ├── js/
│   │   ├── api.js               # Kết nối Backend API hoặc chạy bộ máy suy diễn nội bộ giả lập
│   │   ├── main.js              # Quản lý Dark/Light Theme, Sticky Header, Toast, Mobile Menu
│   │   ├── validation.js        # Kiểm tra tính hợp lệ của thông tin học sinh và điểm số
│   │   ├── home.js              # Script hỗ trợ trang chủ
│   │   ├── consultation.js      # Điều phối Stepper 4 bước, hiệu ứng tính toán của chuyên gia
│   │   ├── result.js            # Vẽ biểu đồ Radar Chart (Chart.js) và hiển thị vết giải thích
│   │   ├── career.js            # Lọc ngành theo lĩnh vực, từ khóa tìm kiếm và tổ hợp xét tuyển
│   │   └── history.js           # Đọc và render lịch sử tư vấn từ LocalStorage
│   └── images/                  # Thư mục hình ảnh & logo
├── components/
│   ├── header.html              # Thanh điều hướng đầu trang
│   ├── navbar.html              # Component thanh menu phụ
│   ├── footer.html              # Chân trang với thông tin liên hệ và bản quyền
│   ├── sidebar.html             # Bộ lọc ngành nghề nhanh
│   ├── career-card.html         # Mẫu thẻ ngành nghề
│   ├── result-card.html         # Mẫu thẻ kết quả tư vấn kèm vết suy diễn
│   └── loading.html             # Modal thông báo tiến trình suy diễn luật
└── pages/
    ├── home.html                # Trang chủ (Homepage)
    ├── consultation.html        # Trang làm trắc nghiệm & nhập điểm tư vấn (4 bước)
    ├── result.html              # Báo cáo kết quả phân tích & biểu đồ RIASEC
    ├── career-list.html         # Danh mục tra cứu toàn bộ các ngành nghề
    ├── career-detail.html       # Chi tiết ngành nghề, cơ hội việc làm, mức lương & luật chuyên gia
    ├── history.html             # Xem lại các phiên tư vấn đã lưu
    ├── about.html               # Tài liệu về kiến trúc hệ chuyên gia & thuật toán
    └── 404.html                 # Trang báo lỗi đường dẫn
```

---

## 🚀 Các Điểm Nhấn Công Nghệ & Trải Nghiệm Người Dùng

1. **Chuẩn kiến trúc Hệ Chuyên Gia (Rule-Based Expert System):**
   - Hỗ trợ mô hình hóa **Sự kiện (Facts)**: Học lực 8 môn văn hóa THPT, mã tính cách Holland, nguyện vọng môi trường làm việc và học phí.
   - Cơ chế **Vết suy diễn (Explanation Facility)**: Cho phép học sinh và phụ huynh xem rõ ràng lý do hệ thống đưa ra quyết định thông qua danh sách các luật đã kích hoạt (*Fired Rules*).
2. **Giao diện đa nền tảng & Chế độ Sáng/Tối (Dark/Light Mode):**
   - Tối ưu hóa độ tương phản màu sắc học đường hiện đại.
   - Nút chuyển đổi Dark Mode lưu trạng thái trực tiếp vào `localStorage`.
3. **Độc lập và Linh hoạt (Fallback Engine):**
   - Khi Backend Python/FastAPI chưa khởi chạy, Frontend tích hợp sẵn bộ máy suy diễn nội bộ `ExpertInferenceEngine` tại [api.js](file:///d:/EXPERT_SYSTEM_CAREER/Frontend/assets/js/api.js) giúp giao diện có thể chạy trực tiếp ngay khi mở file trên trình duyệt!
4. **Biểu đồ Radar tương tác (Chart.js):**
   - Trực quan hóa 6 nhóm tính cách Holland (R, I, A, S, E, C) sống động, đẹp mắt.

---

## 💻 Cách Khởi Chạy

Bạn có thể chạy trực tiếp bằng cách:
1. Mở file [index.html](file:///d:/EXPERT_SYSTEM_CAREER/Frontend/index.html) bằng bất kỳ trình duyệt web nào (Chrome, Edge, Firefox, Cốc Cốc).
2. Hoặc sử dụng extension **Live Server** trong VS Code / Antigravity IDE để có trải nghiệm hot-reload tốt nhất.
