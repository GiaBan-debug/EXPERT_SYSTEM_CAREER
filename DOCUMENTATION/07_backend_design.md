# 07 – Thiết Kế Hệ Thống Backend (Backend Design)

## 1. Công nghệ & Thư viện
- **Framework:** FastAPI (Python 3.10+) với ASGI Server Uvicorn.
- **Xác thực:** PyJWT kết hợp SHA-256 hash.
- **Validation:** Pydantic v2 schemas.
- **Kiến trúc:** Layered Architecture chia tách rành mạch:
  - `api/`: Tiếp nhận HTTP Request, routing, status code.
  - `services/`: Xử lý nghiệp vụ logic, kết nối giữa Repository và Lõi Hệ chuyên gia.
  - `database/repositories/`: Tương tác đọc/ghi CSDL và tệp tin JSON.
  - `expert_system/`: Lõi suy diễn độc lập với framework Web.

## 2. Danh sách các Router chính
- `health_routes.py`: Kiểm tra sức khỏe hệ thống (`/api/health`).
- `career_routes.py`: Danh mục và chi tiết ngành nghề (`/api/careers`).
- `consultation_routes.py`: Tiếp nhận dữ liệu học sinh và thực hiện suy diễn (`/api/consultations/evaluate`).
- `history_routes.py`: Truy vấn lịch sử tư vấn (`/api/history`).
- `admin_routes.py`: Quản lý tập luật và thống kê hệ thống (`/api/admin`).
- `auth_routes.py`: Đăng ký, đăng nhập và lấy thông tin user (`/api/auth`).
