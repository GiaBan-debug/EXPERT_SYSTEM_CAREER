# 05 – Thiết Kế Cơ Sở Dữ Liệu (Database Design)

## 1. Mô hình thực thể - liên kết (ERD)
Cơ sở dữ liệu được tổ chức trên hệ quản trị SQLite, bao gồm 5 bảng chính:
- **`users`:** Lưu thông tin tài khoản đăng nhập và phân quyền (`id`, `username`, `password_hash`, `full_name`, `email`, `role`, `created_at`).
- **`students`:** Lưu trữ thông tin cá nhân của học sinh THPT (`id`, `user_id`, `full_name`, `grade`, `school`, `region`, `track`, `created_at`).
- **`career_categories`:** Danh mục 6 khối ngành chuẩn (`id`, `name`, `description`, `icon`).
- **`careers`:** Danh mục chi tiết các ngành nghề đào tạo (`id`, `code`, `name`, `category_id`, `description`, `riasec_primary`, `riasec_code`, `required_blocks`, `top_universities`, `average_salary`, `market_trend`, `icon`).
- **`consultations`:** Nhật ký các phiên tư vấn đã thực hiện (`id`, `student_id`, `user_id`, `dominant_code`, `scores_json`, `riasec_json`, `preferences_json`, `recommendations_json`, `explanation_json`, `created_at`).
- **`system_rules`:** Lưu trữ tập luật tri thức dạng bảng SQL bổ trợ (`id`, `name`, `description`, `category`, `conditions_json`, `conclusion_json`, `priority`, `confidence`, `enabled`).

## 2. Cấu trúc lưu trữ tri thức JSON
Ngoài CSDL quan hệ, các tệp JSON trong `DATABASE/data/` đóng vai trò là kho tri thức trực tiếp cho động cơ suy diễn:
- `rules.json`: Lưu trữ 35+ luật sản xuất 2 tầng.
- `fact_conventions.json`: Quy ước tên thuộc tính, kiểu dữ liệu và miền giá trị hợp lệ.
