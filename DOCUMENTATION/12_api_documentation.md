# 12 – Tài Liệu Đặc Tả API (API Documentation)

## 1. Cấu hình chung
- **Base URL:** `http://127.0.0.1:8000/api`
- **Định dạng dữ liệu:** JSON (`Content-Type: application/json`)
- **Tài liệu trực quan:** Truy cập Swagger UI tại `http://127.0.0.1:8000/docs`

## 2. Danh sách Endpoints

| Phương thức | Endpoint | Mô tả | Quyền truy cập |
|---|---|---|---|
| `GET` | `/health` | Kiểm tra trạng thái máy chủ | Công khai |
| `GET` | `/careers` | Danh sách toàn bộ ngành nghề | Công khai |
| `GET` | `/careers/categories` | Danh sách 6 nhóm ngành lớn | Công khai |
| `GET` | `/careers/{id}` | Chi tiết một ngành nghề cụ thể | Công khai |
| `POST` | `/consultations/evaluate` | Gửi hồ sơ và nhận kết quả suy diễn | Công khai / User |
| `GET` | `/history` | Lịch sử các phiên tư vấn | Công khai / User |
| `POST` | `/auth/register` | Đăng ký tài khoản mới | Công khai |
| `POST` | `/auth/login` | Đăng nhập hệ thống | Công khai |
| `GET` | `/auth/me` | Lấy thông tin user hiện tại | User / Admin |
| `GET` | `/admin/stats` | Thống kê số liệu hệ thống | Admin |
| `GET` | `/admin/rules` | Danh sách tập luật tri thức | Admin |
| `PATCH` | `/admin/rules/{id}/toggle` | Bật / Tắt một luật | Admin |
| `POST` | `/admin/rules` | Thêm luật tri thức mới | Admin |
| `DELETE` | `/admin/rules/{id}` | Xóa luật khỏi cơ sở tri thức | Admin |
