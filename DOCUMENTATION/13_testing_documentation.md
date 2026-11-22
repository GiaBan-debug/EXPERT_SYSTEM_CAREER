# 13 – Tài Liệu Kiểm Thử Hệ Thống (Testing Documentation)

## 1. Chiến lược kiểm thử
Hệ thống áp dụng phương pháp kiểm thử tự động toàn diện từ tầng Unit Test, Integration Test đến API End-to-end Test bằng framework `pytest`.

## 2. Báo cáo các bộ Test Suite
1. **`test_facts.py` (3 test cases):** Kiểm tra tạo Fact, chuyển đổi payload học sinh và kiểm tra hợp lệ của thuộc tính theo quy ước.
2. **`test_student_facts.py` (7 test cases):** Kiểm thử nâng cao việc bóc tách điểm số, tổ hợp môn GDPT mới và mã Holland.
3. **`test_knowledge_base.py` (68 test cases):** Kiểm tra cú pháp luật, kiểm tra tính đầy đủ, trùng lặp ID, validator và các hàm CRUD của RuleManager.
4. **`test_inference.py` (47 test cases):** Kiểm thử bộ máy suy diễn tiến, kiểm tra điều kiện logic (AND/OR/NOT), chuỗi suy luận nhiều bước và cơ chế dừng fixed-point.
5. **`test_conflict_resolution.py` (3 test cases):** Kiểm tra phát hiện xung đột và thuật toán xếp hạng nghề nghiệp.
6. **`test_explanation.py` (1 test case):** Kiểm tra sinh vết giải thích và định dạng chuỗi tự nhiên.
7. **`test_consultation_api.py` (3 test cases):** Kiểm thử luồng gọi API đánh giá tư vấn qua TestClient.
8. **`test_auth_api.py` (4 test cases):** Kiểm thử đăng ký, băm mật khẩu và đăng nhập phân quyền.
9. **`test_admin_api.py` (3 test cases):** Kiểm thử API quản trị luật và thống kê hệ thống.
10. **`test_integration.py` (1 test case):** Kiểm thử tích hợp toàn trình End-to-end.

**Tổng kết:** **150+ test cases** tự động đạt tỷ lệ Pass 100%.
