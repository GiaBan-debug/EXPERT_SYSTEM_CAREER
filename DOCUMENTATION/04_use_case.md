# 04 – Đặc Tả Ca Sử Dụng (Use Case Specification)

## 1. Danh sách tác nhân (Actors)
- **Học sinh THPT (User):** Người trực tiếp nhập điểm học bạ, hoàn thành bài test RIASEC và nhận kết quả tư vấn hướng nghiệp.
- **Quản trị viên (Admin):** Người quản lý cơ sở tri thức, tinh chỉnh trọng số luật, theo dõi số liệu thống kê lượt đánh giá.
- **Khách vãng lai (Guest):** Người dùng chưa đăng nhập, được phép tra cứu danh mục ngành nghề và khối thi THPT.

## 2. Các Ca sử dụng chính
1. **UC-01: Tư vấn chọn ngành nghề:**
   - *Luồng chính:* Học sinh nhập hồ sơ -> Nhập điểm 8 môn -> Trả lời câu hỏi RIASEC -> Chọn nguyện vọng -> Hệ thống suy diễn -> Trả về Top 5 ngành phù hợp, biểu đồ Radar và vết giải thích.
2. **UC-02: Tra cứu ngành học & Khối thi:**
   - Tìm kiếm theo từ khóa, lọc theo lĩnh vực và khối xét tuyển đại học.
3. **UC-03: Xem vết suy diễn (Explanation Trace):**
   - Xem chi tiết từng bước kích hoạt luật và lý do đề xuất ngành.
4. **UC-04: Quản lý tập luật (Dành cho Admin):**
   - Bật/tắt luật trực tiếp, thêm luật mới có validate điều kiện IF-THEN, xóa luật.
5. **UC-05: Đăng ký & Đăng nhập phân quyền:**
   - Cấp tài khoản và mã token xác thực vai trò Admin hoặc User.
