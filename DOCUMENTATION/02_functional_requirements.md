# 02 – Yêu Cầu Chức Năng & Phi Chức Năng (Requirements Specification)

## 1. Yêu cầu chức năng (Functional Requirements)
- **FR-01: Quản lý hồ sơ học sinh:** Nhập họ tên, khối lớp (10, 11, 12), trường THPT, khu vực địa lý và định hướng tổ hợp GDPT mới.
- **FR-02: Nhập điểm học bạ:** Nhập điểm trung bình 8 môn văn hóa (Toán, Lý, Hóa, Sinh, Văn, Anh, Tin, Sử/Địa) theo thang điểm 10.
- **FR-03: Trắc nghiệm RIASEC:** Trả lời bộ câu hỏi tương ứng 6 nhóm tính cách Holland (Thực tế, Nghiên cứu, Nghệ thuật, Xã hội, Quản trị, Nghiệp vụ) theo thang đo Likert 5 mức độ.
- **FR-04: Động cơ suy diễn tiến:** Tự động kích hoạt các luật IF-THEN 2 tầng để suy luận ra năng lực, sở thích và đề xuất nhóm ngành.
- **FR-05: Giải quyết xung đột & Xếp hạng:** Xử lý tập luật kích hoạt đồng thời theo độ tin cậy (*Confidence*), độ ưu tiên (*Priority*) và độ cụ thể (*Specificity*).
- **FR-06: Vết suy diễn (Explanation Trace):** Hiển thị chi tiết từng bước lập luận và các luật cụ thể đã kích hoạt (*Fired Rules*).
- **FR-07: Quản trị tri thức (Admin Control):** Cho phép Quản trị viên Bật/Tắt luật, thêm luật mới có kiểm tra hợp lệ (*Validation*) và xóa luật.
- **FR-08: Đăng nhập & Phân quyền (Auth & RBAC):** Xác thực tài khoản Admin và Học sinh qua JWT Token, bảo vệ trang quản trị.

## 2. Yêu cầu phi chức năng (Non-Functional Requirements)
- **Hiệu năng:** Thời gian suy diễn dưới 100ms trên một lượt đánh giá.
- **Độ tin cậy:** Cơ chế khúc xạ (*Refraction*) ngăn ngừa 100% vòng lặp vô hạn.
- **Bảo mật:** Mật khẩu người dùng được băm SHA-256; token JWT có thời hạn hợp lệ.
- **Trải nghiệm người dùng:** Giao diện Responsive tối ưu trên mọi màn hình, hỗ trợ Dark/Light Theme.
