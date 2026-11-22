# 11 – Vết Suy Diễn & Bộ Giải Thích (Explanation Trace)

## 1. Tầm quan trọng của Bộ giải thích
Khác với các mô hình học máy dạng hộp đen (Black-box), điểm mạnh vượt trội của Hệ chuyên gia dựa trên luật là khả năng **tự giải thích (Explanation Facility)**. Học sinh và phụ huynh có quyền biết vì sao ngành học này lại được hệ thống gợi ý đầu tiên.

## 2. Cấu trúc Vết suy diễn (Execution Trace)
Mỗi bước bắn luật được ghi nhận thành một đối tượng `FiredStep`:
- **`step`:** Thứ tự bước suy luận.
- **`rule_id` & `rule_name`:** Mã và tên luật đã bắn.
- **`priority` & `confidence`:** Trọng số của luật.
- **`new_facts`:** Các dữ kiện trung gian mới được sinh ra.
- **`conflict_set`:** Danh sách các luật cùng kích hoạt tại chu kỳ đó.
- **`explanation`:** Diễn giải ngôn ngữ tự nhiên về lý do thỏa mãn điều kiện.

Bộ định dạng `ExplanationFormatter` sẽ tổng hợp các bước này thành các luận điểm mạch lạc trên giao diện người dùng.
