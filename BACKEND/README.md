# Backend - Hệ Chuyên Gia Tư Vấn Chọn Ngành/Nghề THPT

Hệ thống Backend được xây dựng bằng Python và FastAPI, cung cấp API cho Hệ chuyên gia tư vấn hướng nghiệp học sinh THPT dựa trên mô hình tâm lý RIASEC John Holland và thuật toán Suy diễn tiến (Forward Chaining).

## 1. Cấu trúc thư mục

```
BACKEND/
├── app/
│   ├── __init__.py           # Khởi tạo FastAPI App, CORS middleware
│   ├── api/                  # Tầng REST API Routes
│   │   ├── health_routes.py        # Kiểm tra trạng thái hệ thống
│   │   ├── career_routes.py        # API tra cứu ngành nghề, danh mục
│   │   ├── consultation_routes.py  # API tư vấn & suy diễn chuyên gia
│   │   └── history_routes.py       # API lịch sử phiên tư vấn
│   ├── database/             # Tầng kết nối & cấu hình CSDL
│   │   ├── db.py                   # Kết nối SQLite
│   │   ├── init_db.py              # Khởi tạo CSDL từ schema & seed
│   │   └── repositories/           # Tầng Repository thao tác dữ liệu
│   ├── expert_system/        # LÕI HỆ CHUYÊN GIA
│   │   ├── facts/                  # Biểu diễn & kiểm tra Fact (Thành viên 1)
│   │   ├── knowledge_base/         # Quản lý & kiểm tra luật (Thành viên 2)
│   │   ├── inference/              # Bộ máy suy diễn tiến (Thành viên 3)
│   │   ├── conflict_resolution/    # Giải quyết xung đột & xếp hạng (Thành viên 4)
│   │   └── explanation/            # Vết suy diễn & giải thích (Thành viên 5)
│   ├── models/               # Data classes (Rule, Career, Student, Consultation)
│   ├── schemas/              # Pydantic schemas cho API Request/Response
│   ├── services/             # Nghiệp vụ điều phối chính
│   └── utils/                # Logger, Response Handler, Constants
├── tests/                    # 158+ Unit & Integration Test Cases
├── config.py                 # Cấu hình môi trường (Host, Port, CORS)
└── run.py                    # Điểm khởi chạy Uvicorn Server
```

## 2. Hướng dẫn chạy

1. Cài đặt thư viện:
   ```bash
   pip install -r requirements.txt
   ```
2. Khởi chạy máy chủ API:
   ```bash
   python run.py
   ```
   Server sẽ lắng nghe tại: `http://127.0.0.1:8000`. Xem tài liệu Swagger UI tại: `http://127.0.0.1:8000/docs`.

3. Chạy toàn bộ bài kiểm thử tự động:
   ```bash
   pytest tests
   ```
