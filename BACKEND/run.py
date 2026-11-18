"""Điểm khởi chạy máy chủ Backend Uvicorn."""
import uvicorn
from config import HOST, PORT, DEBUG

if __name__ == "__main__":
    print(f"🚀 Khởi chạy máy chủ tại http://{HOST}:{PORT}")
    uvicorn.run(
        "app:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
    )
