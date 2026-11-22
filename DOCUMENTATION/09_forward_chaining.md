# 09 – Thuật Toán Suy Diễn Tiến (Forward Chaining Algorithm)

## 1. Nguyên lý hoạt động
Thuật toán Suy diễn tiến bắt đầu từ các dữ kiện đã biết (Facts trong Working Memory) để suy ra các dữ kiện mới cho đến khi đạt được mục tiêu (đề xuất nhóm ngành) hoặc không còn luật nào có thể kích hoạt:

```
BƯỚC 1: Nạp tập Facts ban đầu vào Working Memory (WM).
BƯỚC 2: Lặp chu kỳ (Iteration):
         a. Tìm tập luật xung đột (Conflict Set) gồm các luật:
            - Đang ở trạng thái BẬT (enabled = true).
            - Chưa từng được bắn trước đó (Refraction).
            - Mọi điều kiện IF đều thỏa mãn trên WM hiện tại.
         b. Nếu Conflict Set rỗng -> DỪNG (Fixed Point).
         c. Chọn luật tốt nhất (Best Rule) thông qua Conflict Resolver.
         d. Bắn luật (Fire Rule):
            - Nếu conclusion type = "fact" -> Thêm Fact trung gian vào WM.
            - Nếu conclusion type = "recommendation" -> Ghi vào danh sách đề xuất.
            - Ghi lại bước thực thi vào Vết suy diễn (Execution Trace).
BƯỚC 3: Trả về kết quả và danh sách đề xuất.
```

## 2. Cơ chế ngăn chặn vòng lặp vô hạn (Refraction)
Mỗi luật chỉ được bắn tối đa một lần duy nhất trong suốt một phiên suy diễn. Cơ chế này đảm bảo thuật toán luôn dừng lại sau hữu hạn bước (thường từ 2 - 5 bước).
