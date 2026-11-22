# 10 – Cơ Chế Giải Quyết Xung Đột (Conflict Resolution)

## 1. Bản chất xung đột trong Hệ Chuyên Gia
Trong mỗi chu kỳ suy diễn, thường có nhiều luật cùng thỏa mãn tiền đề IF (tạo thành tập xung đột - *Conflict Set*). Việc lựa chọn luật nào bắn trước có thể ảnh hưởng đến các bước suy luận kế tiếp.

## 2. Chiến lược 4 tiêu chí giải quyết xung đột
Động cơ suy diễn áp dụng chiến lược sắp xếp ưu tiên chặt chẽ:
1. **Độ tin cậy (Confidence):** Tiêu chí chính. Luật có hệ số tin cậy cao hơn ($0.0 < CF \le 1.0$) sẽ được ưu tiên bắn trước.
2. **Độ ưu tiên (Priority):** Tiêu chí phụ. Khi hai luật có độ tin cậy bằng nhau, luật có độ ưu tiên cao hơn (mức từ 1 đến 10 do chuyên gia quy định) sẽ được chọn.
3. **Độ cụ thể (Specificity):** Luật có nhiều điều kiện ràng buộc khắt khe hơn sẽ được ưu tiên hơn luật tổng quát.
4. **Thứ tự ID (Lexicographical ID):** Tiêu chí phân định cuối cùng đảm bảo tính tất định (Deterministic) của thuật toán.
