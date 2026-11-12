# 08 – Cơ sở tri thức (Knowledge Base)

Tài liệu của **Thành viên 2**. Mô tả cách biểu diễn luật IF–THEN, ý nghĩa từng trường, quy ước Fact dùng chung, và bộ 35 luật hiện có.

## 1. Tổng quan

| Thành phần | File |
|---|---|
| Mô hình luật (`Rule`, `Condition`, `Conclusion`) | `BACKEND/app/models/rule.py` |
| Bảng quy ước Fact (dùng chung với Thành viên 1) | `DATABASE/data/fact_conventions.json` |
| Đọc bảng quy ước | `knowledge_base/fact_conventions.py` |
| Kiểm tra luật | `knowledge_base/rule_validator.py` |
| Nạp luật từ JSON | `knowledge_base/rule_loader.py` |
| Quản lý tập luật (bật/tắt/sửa/thêm/xóa/lưu) | `knowledge_base/rule_manager.py` |
| Bộ luật | `DATABASE/data/rules.json` |
| Unit test | `BACKEND/tests/test_knowledge_base.py` |

Bộ luật có **2 tầng** để forward chaining suy diễn được nhiều bước:

1. **Tầng 1 – luật sinh Fact trung gian** (`ABL-*`, `INT-*`): từ điểm môn và RIASEC suy ra *năng lực* (`ability.*`) và *sở thích* (`interest.*`).
2. **Tầng 2 – luật đề xuất nhóm ngành** (`GRP-*`): dùng cả Fact đầu vào lẫn Fact trung gian để đề xuất nhóm ngành.

## 2. Cấu trúc một luật

```json
{
  "id": "GRP-01",
  "name": "CNTT: logic cao + thích công nghệ",
  "description": "Giải thích ngắn bằng tiếng Việt",
  "category": "career_group",
  "conditions": [
    {"attribute": "ability.logic", "operator": "==", "value": "high"},
    {"attribute": "interest.tech", "operator": "==", "value": "high"}
  ],
  "conclusion": {"type": "recommendation", "career_group": "CNTT", "careers": ["it_software", "ai_data"]},
  "priority": 9,
  "confidence": 0.95,
  "enabled": true
}
```

| Trường | Bắt buộc | Ý nghĩa |
|---|---|---|
| `id` | ✔ | Mã luật duy nhất, dạng `AAA-01` (`ABL`/`INT`/`GRP`…). |
| `name` | ✔ | Tên ngắn gọn, hiển thị trong phần giải thích. |
| `description` | | Mô tả vì sao luật có ý nghĩa. |
| `category` | | Nhãn phân loại (`ability`, `interest`, `career_group`). |
| `conditions` | ✔ | Phần **IF**: danh sách điều kiện, **tất cả** phải đúng (AND). Mỗi điều kiện = `thuộc_tính – toán_tử – giá_trị`, cùng dạng với Fact của Thành viên 1. |
| `conclusion` | ✔ | Phần **THEN**: xem mục 3. |
| `priority` | ✔ | **Độ ưu tiên**, số nguyên 1–10, **cao hơn = ưu tiên hơn**. Tiêu chí phụ khi xung đột (xem mục 4). |
| `confidence` | ✔ | **Độ tin cậy**, số thực trong (0, 1]. Tiêu chí chính khi xung đột (xem mục 4). |
| `enabled` | | `true`/`false`, mặc định `true`. Luật tắt không tham gia suy diễn. |

**Toán tử**: số dùng `== != > >= < <=`; thuộc tính liệt kê dùng `== != in not_in` (với `in`/`not_in`, `value` là danh sách).

## 3. Hai loại kết luận (THEN)

| `type` | Trường | Tác dụng |
|---|---|---|
| `fact` | `attribute`, `value` | Thêm **Fact trung gian** vào tập Facts để luật khác dùng tiếp. Chỉ được gán cho thuộc tính `derived`; luật **không được** kết luận ra dữ kiện đầu vào. |
| `recommendation` | `career_group`, `careers` (tùy chọn) | Đề xuất một **nhóm ngành** (và các ngành cụ thể thuộc nhóm đó). |

## 4. Priority khác Confidence thế nào

| | `priority` | `confidence` |
|---|---|---|
| Là gì | Thứ tự ưu tiên do người xây dựng tri thức quy định | Mức chắc chắn của kết luận |
| Kiểu / miền | Nguyên, 1–10 | Thực, (0, 1] |
| Dùng để | Tiêu chí **phụ** khi xung đột: chỉ quyết định khi confidence bằng nhau | Tiêu chí **chính** khi xung đột và xếp hạng: cao hơn thắng |
| Ví dụ | Luật 2 điều kiện mạnh (`GRP-01`) = 9; luật theo nguyện vọng (`GRP-11`) = 3 | `GRP-01` = 0.95; `GRP-11` = 0.65 |

Hai giá trị **độc lập**: một luật có thể ưu tiên cao nhưng độ tin cậy vừa, và ngược lại.

**Thứ tự so sánh khi nhiều luật xung đột** (khớp với code của Thành viên 4): so **confidence** trước, **cao hơn thắng**; nếu bằng nhau mới so **priority**, cao hơn thắng. Ví dụ: luật A có priority 9, confidence 0.50 và luật B có priority 5, confidence 0.90 → luật **B** thắng vì tin cậy cao hơn. Chi tiết chiến lược do Thành viên 4 công bố trong `10_conflict_resolution.md`.

Quy ước gán điểm đang dùng:

| Loại luật | priority | confidence |
|---|---|---|
| Luật sinh Fact trung gian (`ABL`, `INT`) | 5 | 0.75 – 0.90 |
| Đề xuất: ≥ 2 Fact trung gian mạnh khớp nhau | 8 – 9 | 0.90 – 0.95 |
| Đề xuất: Fact trung gian + nguyện vọng / điểm môn | 6 – 7 | 0.80 – 0.90 |
| Đề xuất: chỉ dựa trên nguyện vọng (`pref.priority`) | 3 – 4 | 0.65 – 0.70 |

## 5. Quy ước Fact (thỏa thuận với Thành viên 1)

Tên thuộc tính khớp với payload frontend (`student`, `scores`, `riasec`, `preferences`) theo dạng `nhóm.tên`. Nguồn thật: `DATABASE/data/fact_conventions.json`.

**Fact đầu vào** (`source: input`)

| Thuộc tính | Ý nghĩa | Miền giá trị |
|---|---|---|
| `score.math` | Điểm Toán | số 1–10 |
| `score.physics` | Điểm Vật lý | số 1–10 |
| `score.chemistry` | Điểm Hóa học | số 1–10 |
| `score.biology` | Điểm Sinh học | số 1–10 |
| `score.literature` | Điểm Ngữ văn | số 1–10 |
| `score.english` | Điểm Tiếng Anh | số 1–10 |
| `score.informatics` | Điểm Tin học | số 1–10 |
| `score.history` | Điểm Lịch sử | số 1–10 |
| `riasec.R` | RIASEC - Thực tế (Realistic) | số 0–100 |
| `riasec.I` | RIASEC - Nghiên cứu (Investigative) | số 0–100 |
| `riasec.A` | RIASEC - Nghệ thuật (Artistic) | số 0–100 |
| `riasec.S` | RIASEC - Xã hội (Social) | số 0–100 |
| `riasec.E` | RIASEC - Quản lý (Enterprising) | số 0–100 |
| `riasec.C` | RIASEC - Nghiệp vụ (Conventional) | số 0–100 |
| `student.track` | Tổ hợp môn GDPT mới | khoa_hoc_tu_nhien, khoa_hoc_xa_hoi, cong_nghe_nghe_thuat |
| `student.grade` | Khối lớp | 10, 11, 12 |
| `student.region` | Khu vực | north, central, south, abroad |
| `pref.environment` | Môi trường làm việc mong muốn | tech, medical, creative, business |
| `pref.tuition` | Mức học phí | standard, high, international, free |
| `pref.priority` | Ưu tiên nghề nghiệp | high_salary, stability, passion, abroad |

**Fact trung gian** (`source: derived`, do luật tầng 1 sinh ra)

| Thuộc tính | Ý nghĩa | Miền giá trị |
|---|---|---|
| `ability.logic` | Năng lực tư duy logic - tính toán | low, medium, high |
| `ability.natural_science` | Năng lực khoa học tự nhiên | low, medium, high |
| `ability.language` | Năng lực ngôn ngữ | low, medium, high |
| `ability.social_science` | Năng lực khoa học xã hội | low, medium, high |
| `interest.tech` | Sở thích công nghệ | low, medium, high |
| `interest.health` | Sở thích chăm sóc sức khỏe | low, medium, high |
| `interest.art` | Sở thích nghệ thuật | low, medium, high |
| `interest.business` | Sở thích kinh doanh | low, medium, high |
| `interest.management` | Sở thích quản lý - vận hành | low, medium, high |
| `interest.education` | Sở thích giáo dục | low, medium, high |
| `interest.engineering` | Sở thích kỹ thuật | low, medium, high |

**Nhóm ngành & ngành**

| Mã nhóm | Tên | Ngành (mã trong frontend) |
|---|---|---|
| `CNTT` | Công nghệ Thông tin | it_software, ai_data |
| `YDUOC` | Y Dược & Chăm sóc Sức khỏe | medical_doctor |
| `KINHTE` | Kinh tế, Marketing & Quản lý | digital_marketing, logistics_supply |
| `NGHETHUAT` | Nghệ thuật & Sáng tạo | graphic_design |
| `KYTHUAT` | Kỹ thuật & Công nghệ | automation_eng |
| `GIAODUC` | Giáo dục & Xã hội | pedagogy_edu |

> Nếu Thành viên 1 đổi tên thuộc tính hoặc miền giá trị, chỉ cần sửa `fact_conventions.json` rồi chạy lại test; validator sẽ chỉ ra luật nào không còn khớp.

## 6. Kiểm tra luật (RuleValidator)

Luật bị **từ chối** khi: thiếu trường bắt buộc hoặc có trường lạ; `id` sai định dạng; thuộc tính không có trong bảng quy ước; toán tử không hợp kiểu; giá trị ngoài miền; điều kiện tự mâu thuẫn (vd `math >= 8` và `math < 5`); kết luận gán cho dữ kiện đầu vào hoặc ngành không thuộc nhóm; `priority` ngoài 1–10 hoặc không nguyên; `confidence` ngoài (0, 1].

Ở mức cả tập luật: **trùng `id`** hoặc **trùng nội dung** (cùng điều kiện + kết luận, không phụ thuộc thứ tự điều kiện) → luật xuất hiện sau bị loại. **Cảnh báo** (không chặn) khi một điều kiện dùng Fact trung gian mà không luật nào đang bật có thể sinh ra giá trị đó.

## 7. Cách dùng

```python
from app.expert_system.knowledge_base import RuleManager

mgr = RuleManager.from_file()            # mặc định đọc DATABASE/data/rules.json
print(mgr.last_report.summary())         # "rules.json: nạp 35/35 luật, 0 lỗi, 0 cảnh báo"

rules = mgr.active_rules()               # tập luật cho bộ suy diễn (Thành viên 3)
mgr.disable_rule("GRP-05")               # tắt luật
mgr.update_rule("GRP-01", {"confidence": 0.97})
mgr.add_rule({...})                     # kiểm tra trước khi thêm, lỗi -> RuleValidationError
mgr.save()                               # ghi lại rules.json
```

`RuleManager.from_file(strict=True)` sẽ raise `RuleLoadError` nếu có bất kỳ luật lỗi nào (nên dùng khi khởi động server để phát hiện sớm).

## 8. Bàn giao cho các thành viên khác

| Thành viên | Dùng gì từ Knowledge Base |
|---|---|
| 1 | Đối chiếu `fact_conventions.json` với `fact_schema.py`; tên thuộc tính trong Facts phải trùng `attribute` trong luật. |
| 3 | `RuleManager.active_rules()` → danh sách `Rule`; mỗi `Rule.conditions` là `Condition(attribute, operator, value)`; `Rule.conclusion.type` quyết định THEN thêm Fact hay đề xuất nhóm ngành. |
| 4 | `Rule.to_activation_dict()` trả về dict phẳng (`id`, `conclusion` là chuỗi mã nhóm ngành, `priority`, `confidence`, `description`) để đưa thẳng vào `ConflictDetector`. Luật sinh Fact trung gian có `conclusion` dạng `"ability.logic=high"` nên nên lọc `conclusion_type == "recommendation"` trước khi xếp hạng. |
| 5 | `Rule.id`, `name`, `description` để tạo giải thích; `Rule.to_dict()` để tuần tự hóa JSON. |

## 9. Danh sách 35 luật

| Mã | Tên | IF (AND) | THEN | Priority | Confidence |
|---|---|---|---|---|---|
| ABL-01 | Tư duy logic cao (Toán + Tin) | `score.math >= 8` VÀ `score.informatics >= 7.5` | THÊM FACT `ability.logic = high` | 5 | 0.90 |
| ABL-02 | Tư duy logic cao (Toán + Lý) | `score.math >= 8` VÀ `score.physics >= 8` | THÊM FACT `ability.logic = high` | 5 | 0.90 |
| ABL-03 | Tư duy logic trung bình | `score.math >= 5` VÀ `score.math < 8` | THÊM FACT `ability.logic = medium` | 5 | 0.80 |
| ABL-04 | Tư duy logic thấp | `score.math < 5` | THÊM FACT `ability.logic = low` | 5 | 0.80 |
| ABL-05 | Khoa học tự nhiên cao | `score.chemistry >= 8` VÀ `score.biology >= 8` | THÊM FACT `ability.natural_science = high` | 5 | 0.90 |
| ABL-06 | Khoa học tự nhiên trung bình | `score.chemistry >= 6.5` VÀ `score.chemistry < 8` VÀ `score.biology >= 6.5` | THÊM FACT `ability.natural_science = medium` | 5 | 0.75 |
| ABL-07 | Năng lực ngôn ngữ cao | `score.literature >= 7.5` VÀ `score.english >= 7.5` | THÊM FACT `ability.language = high` | 5 | 0.85 |
| ABL-08 | Khoa học xã hội cao | `score.literature >= 8` VÀ `score.history >= 7.5` | THÊM FACT `ability.social_science = high` | 5 | 0.85 |
| INT-01 | Thích công nghệ | `riasec.I >= 80` VÀ `riasec.R >= 60` | THÊM FACT `interest.tech = high` | 5 | 0.85 |
| INT-02 | Thích chăm sóc sức khỏe | `riasec.I >= 80` VÀ `riasec.S >= 60` | THÊM FACT `interest.health = high` | 5 | 0.85 |
| INT-03 | Thích nghệ thuật | `riasec.A >= 80` | THÊM FACT `interest.art = high` | 5 | 0.90 |
| INT-04 | Thích kinh doanh | `riasec.E >= 80` | THÊM FACT `interest.business = high` | 5 | 0.85 |
| INT-05 | Thích giáo dục - giúp đỡ người khác | `riasec.S >= 80` | THÊM FACT `interest.education = high` | 5 | 0.85 |
| INT-06 | Thích kỹ thuật - thực hành | `riasec.R >= 80` | THÊM FACT `interest.engineering = high` | 5 | 0.85 |
| INT-07 | Thích quản lý - vận hành | `riasec.C >= 80` VÀ `riasec.E >= 60` | THÊM FACT `interest.management = high` | 5 | 0.80 |
| GRP-01 | CNTT: logic cao + thích công nghệ | `ability.logic == high` VÀ `interest.tech == high` | ĐỀ XUẤT nhóm `CNTT` (it_software, ai_data) | 9 | 0.95 |
| GRP-02 | CNTT: logic cao + môi trường công nghệ | `ability.logic == high` VÀ `pref.environment == tech` | ĐỀ XUẤT nhóm `CNTT` (it_software, ai_data) | 7 | 0.85 |
| GRP-03 | CNTT: giỏi Tin học + thích nghiên cứu | `score.informatics >= 8.5` VÀ `riasec.I >= 70` | ĐỀ XUẤT nhóm `CNTT` (it_software) | 7 | 0.85 |
| GRP-04 | AI & Dữ liệu: Toán xuất sắc | `ability.logic == high` VÀ `score.math >= 9` VÀ `riasec.I >= 80` | ĐỀ XUẤT nhóm `CNTT` (ai_data) | 8 | 0.90 |
| GRP-05 | CNTT: ưu tiên thu nhập cao | `ability.logic == high` VÀ `pref.priority == high_salary` | ĐỀ XUẤT nhóm `CNTT` (it_software, ai_data) | 4 | 0.70 |
| GRP-06 | Y Dược: khoa học tự nhiên cao + thích chăm sóc sức khỏe | `ability.natural_science == high` VÀ `interest.health == high` | ĐỀ XUẤT nhóm `YDUOC` (medical_doctor) | 9 | 0.95 |
| GRP-07 | Y Dược: khoa học tự nhiên cao + môi trường y tế | `ability.natural_science == high` VÀ `pref.environment == medical` | ĐỀ XUẤT nhóm `YDUOC` (medical_doctor) | 7 | 0.85 |
| GRP-08 | Y Dược: tổ hợp KHTN + Sinh giỏi + hướng xã hội | `student.track == khoa_hoc_tu_nhien` VÀ `score.biology >= 8` VÀ `riasec.S >= 60` | ĐỀ XUẤT nhóm `YDUOC` (medical_doctor) | 6 | 0.80 |
| GRP-09 | Nghệ thuật: thích nghệ thuật + môi trường sáng tạo | `interest.art == high` VÀ `pref.environment == creative` | ĐỀ XUẤT nhóm `NGHETHUAT` (graphic_design) | 8 | 0.90 |
| GRP-10 | Nghệ thuật: RIASEC(A) cao + tổ hợp Công nghệ - Nghệ thuật | `riasec.A >= 70` VÀ `student.track == cong_nghe_nghe_thuat` | ĐỀ XUẤT nhóm `NGHETHUAT` (graphic_design) | 6 | 0.80 |
| GRP-11 | Nghệ thuật: ưu tiên đam mê | `pref.priority == passion` VÀ `riasec.A >= 60` | ĐỀ XUẤT nhóm `NGHETHUAT` (graphic_design) | 3 | 0.65 |
| GRP-12 | Kinh tế: thích kinh doanh + ngôn ngữ tốt | `interest.business == high` VÀ `ability.language == high` | ĐỀ XUẤT nhóm `KINHTE` (digital_marketing) | 8 | 0.90 |
| GRP-13 | Kinh tế: môi trường kinh doanh + RIASEC(E) cao | `pref.environment == business` VÀ `riasec.E >= 65` | ĐỀ XUẤT nhóm `KINHTE` (digital_marketing) | 6 | 0.80 |
| GRP-14 | Kinh tế: thích quản lý - vận hành + logic từ trung bình | `interest.management == high` VÀ `ability.logic in [medium, high]` | ĐỀ XUẤT nhóm `KINHTE` (logistics_supply) | 7 | 0.85 |
| GRP-15 | Kinh tế: ưu tiên cơ hội nước ngoài + Tiếng Anh tốt | `pref.priority == abroad` VÀ `score.english >= 8` | ĐỀ XUẤT nhóm `KINHTE` | 3 | 0.65 |
| GRP-16 | Kỹ thuật: thích kỹ thuật + logic cao | `interest.engineering == high` VÀ `ability.logic == high` | ĐỀ XUẤT nhóm `KYTHUAT` (automation_eng) | 8 | 0.90 |
| GRP-17 | Kỹ thuật: RIASEC(R) cao + Vật lý tốt | `riasec.R >= 70` VÀ `score.physics >= 7.5` | ĐỀ XUẤT nhóm `KYTHUAT` (automation_eng) | 6 | 0.80 |
| GRP-18 | Giáo dục: thích giáo dục + khoa học xã hội cao | `interest.education == high` VÀ `ability.social_science == high` | ĐỀ XUẤT nhóm `GIAODUC` (pedagogy_edu) | 8 | 0.90 |
| GRP-19 | Giáo dục: RIASEC(S) cao + quan tâm ngành miễn học phí | `riasec.S >= 70` VÀ `pref.tuition == free` | ĐỀ XUẤT nhóm `GIAODUC` (pedagogy_edu) | 6 | 0.80 |
| GRP-20 | Giáo dục: ưu tiên ổn định + hướng xã hội | `pref.priority == stability` VÀ `riasec.S >= 60` | ĐỀ XUẤT nhóm `GIAODUC` (pedagogy_edu) | 4 | 0.70 |

## 10. Kiểm thử

```bash
cd BACKEND
python -m pytest tests/test_knowledge_base.py -v
```

Bộ test gồm: nạp bộ luật thật (≥ 25 luật, không lỗi, không cảnh báo, đủ nhóm ngành); từ chối luật thiếu trường / sai kiểu / ngoài miền / mâu thuẫn / trùng; loader (file thiếu, JSON hỏng, strict); manager (thêm, sửa, bật/tắt, xóa, lưu rồi nạp lại).
