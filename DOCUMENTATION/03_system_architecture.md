# 03 – Kiến Trúc Hệ Thống (System Architecture)

## 1. Mô hình kiến trúc 3 tầng
Hệ thống được thiết kế theo kiến trúc chuẩn 3 tầng kết hợp Lõi Hệ Chuyên Gia:

```
[FRONTEND CLIENT: HTML5/CSS3/Vanilla JS/Chart.js]
                     │  ▲
        JSON HTTP/REST  │
                     ▼  │
[BACKEND REST API: FastAPI / Python 3.10+]
  ├── Authentication & RBAC Middleware
  ├── Consultation Service (Điều phối)
  └── [LÕI HỆ CHUYÊN GIA - EXPERT ENGINE]
        ├── Fact Base / Working Memory
        ├── Knowledge Base (35+ Rules)
        ├── Forward Chaining Engine
        ├── Conflict Resolver & Ranking
        └── Explanation Facility
                     │  ▲
          SQL / JSON │  │
                     ▼  │
[DATABASE & KNOWLEDGE REPOSITORY: SQLite & JSON Files]
```

## 2. Mô tả các khối thành phần
1. **Tầng Giao diện (Frontend):** Thiết kế dạng Stepper 4 bước, trực quan hóa biểu đồ Radar RIASEC bằng Chart.js, hỗ trợ chế độ Client-side Engine độc lập khi chưa bật Backend.
2. **Tầng Nghiệp vụ (Backend FastAPI):** Tiếp nhận dữ liệu, chuyển đổi thành Facts, nạp tập luật, điều phối suy luận và trả kết quả chuẩn hóa JSON.
3. **Tầng Cơ sở tri thức (Knowledge Base):** Lưu trữ tập luật dạng tệp JSON có cấu trúc, kèm bảng quy ước thuộc tính `fact_conventions.json`.
