# Database Documentation & Knowledge Store

Thư mục `DATABASE` lưu trữ toàn bộ dữ liệu nền tảng và cơ sở tri thức phục vụ Hệ Chuyên Gia Tư Vấn Chọn Ngành/Nghề THPT:

## 1. Cấu trúc thư mục
- `schema.sql`: Định nghĩa cấu trúc bảng SQLite/PostgreSQL (`students`, `careers`, `career_categories`, `consultations`, `system_rules`).
- `seed.sql`: Tập lệnh chèn dữ liệu danh mục ban đầu.
- `data/rules.json`: Cơ sở tri thức chứa 35+ luật sản xuất IF-THEN 2 tầng (suy diễn năng lực, sở thích và kết luận nhóm ngành).
- `data/fact_conventions.json`: Bảng quy ước định danh Fact dùng chung giữa Thành viên 1, 2, 3.
- `data/career_details.json`: Dữ liệu chi tiết 8 ngành đào tạo đại học trọng điểm.
- `data/career_categories.json`: Danh mục 6 khối ngành chuẩn.
- `data/admission_reference.csv`: Điểm chuẩn tham chiếu 2024-2025 theo các tổ hợp khối thi A00, A01, B00, C00, D01...
