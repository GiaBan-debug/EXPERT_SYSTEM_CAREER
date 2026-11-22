"""Tạo các hình ảnh và sơ đồ kỹ thuật chất lượng cao cho dự án EduCareer AI."""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parents[3]
FRONTEND_IMG_DIR = BASE_DIR / "FRONTEND" / "assets" / "images"
REPORT_DIAG_DIR = BASE_DIR / "REPORT" / "diagrams"

os.makedirs(FRONTEND_IMG_DIR, exist_ok=True)
os.makedirs(REPORT_DIAG_DIR, exist_ok=True)


def get_font(size: int):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()


def create_logo():
    """Tạo logo.png nhận diện thương hiệu học đường & AI."""
    img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Nền bo tròn gradient xanh
    for r in range(240, 0, -1):
        alpha = int(255 * (r / 240))
        draw.ellipse([256 - r, 256 - r, 256 + r, 256 + r], fill=(37, 99, 235, 255))
        break

    # Vẽ vòng cung trang trí
    draw.ellipse([20, 20, 492, 492], fill=(30, 58, 138), outline=(96, 165, 250), width=8)
    draw.ellipse([60, 60, 452, 452], fill=(23, 37, 84))

    # Vẽ Mũ cử nhân cách điệu (Graduation Cap)
    draw.polygon([(256, 140), (410, 210), (256, 280), (102, 210)], fill=(96, 165, 250), outline=(255, 255, 255), width=4)
    draw.polygon([(160, 250), (160, 320), (256, 360), (352, 320), (352, 250), (256, 290)], fill=(59, 130, 246))
    draw.line([(400, 210), (400, 340)], fill=(251, 191, 36), width=6)
    draw.ellipse([392, 335, 408, 355], fill=(251, 191, 36))

    # Chữ AI & EduCareer
    font_lg = get_font(42)
    font_sm = get_font(26)
    draw.text((256, 385), "EduCareer AI", fill=(255, 255, 255), anchor="mm", font=font_lg)
    draw.text((256, 430), "EXPERT SYSTEM", fill=(147, 197, 253), anchor="mm", font=font_sm)

    img.save(FRONTEND_IMG_DIR / "logo.png", "PNG")
    print("Created logo.png")


def create_banner():
    """Tạo banner.png cho trang chủ và tài liệu."""
    width, height = 1200, 500
    img = Image.new("RGB", (width, height), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Hiệu ứng ánh sáng
    for i in range(120):
        color = (15 + i // 3, 23 + i // 2, 42 + i)
        draw.line([(0, i * 4), (width, i * 4)], fill=color, width=4)

    # Khung banner hiện đại
    draw.rectangle([40, 40, width - 40, height - 40], outline=(37, 99, 235), width=3)

    font_title = get_font(52)
    font_sub = get_font(28)
    font_desc = get_font(22)

    draw.text((width // 2, 140), "HỆ CHUYÊN GIA TƯ VẤN HƯỚNG NGHIỆP THPT", fill=(255, 255, 255), anchor="mm", font=font_title)
    draw.text((width // 2, 220), "MÔ HÌNH RIASEC HOLLAND & THUẬT TOÁN FORWARD CHAINING", fill=(96, 165, 250), anchor="mm", font=font_sub)
    draw.text((width // 2, 300), "Định hướng chính xác ngành nghề, khối thi và các trường đại học hàng đầu", fill=(203, 213, 225), anchor="mm", font=font_desc)
    draw.text((width // 2, 380), "✦ 6 Nhóm Tính Cách  •  ✦ 35+ Luật Tri Thức  •  ✦ Minh Bạch Vết Suy Diễn", fill=(52, 211, 153), anchor="mm", font=font_desc)

    img.save(FRONTEND_IMG_DIR / "banner.png", "PNG")
    print("Created banner.png")


def create_background():
    """Tạo background.png texture trừu tượng."""
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Lưới grid mờ nhẹ
    grid_size = 60
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=(226, 232, 240), width=1)
    for y in range(0, height, grid_size):
        draw.line([(0, y), (y, height)], fill=(226, 232, 240), width=1)

    # Một vài hình tròn trang trí công nghệ
    draw.ellipse([1400, -200, 2100, 500], fill=(239, 246, 255), outline=(219, 234, 254), width=2)
    draw.ellipse([-200, 600, 500, 1300], fill=(245, 243, 255), outline=(237, 233, 254), width=2)

    img.save(FRONTEND_IMG_DIR / "background.png", "PNG")
    print("Created background.png")


def create_diagram_box(draw, x, y, w, h, title, subtitle, fill_color, border_color):
    draw.rectangle([x, y, x + w, y + h], fill=fill_color, outline=border_color, width=3)
    font_t = get_font(20)
    font_s = get_font(15)
    draw.text((x + w // 2, y + 25), title, fill=(15, 23, 42), anchor="mm", font=font_t)
    if subtitle:
        draw.text((x + w // 2, y + 55), subtitle, fill=(71, 85, 105), anchor="mm", font=font_s)


def create_arrow(draw, start, end, color=(37, 99, 235), width=3):
    draw.line([start, end], fill=color, width=width)
    x1, y1 = start
    x2, y2 = end
    if x1 == x2: # thẳng đứng
        draw.polygon([(x2 - 8, y2 - 12 if y2 > y1 else y2 + 12),
                      (x2 + 8, y2 - 12 if y2 > y1 else y2 + 12),
                      (x2, y2)], fill=color)
    else: # nằm ngang
        draw.polygon([(x2 - 12 if x2 > x1 else x2 + 12, y2 - 8),
                      (x2 - 12 if x2 > x1 else x2 + 12, y2 + 8),
                      (x2, y2)], fill=color)


def create_system_architecture():
    """Tạo diagrams/system_architecture.png."""
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Tiêu đề
    draw.text((w // 2, 40), "SƠ ĐỒ KIẾN TRÚC TỔNG THỂ HỆ CHUYÊN GIA EDUCAREER AI", fill=(15, 23, 42), anchor="mm", font=get_font(28))

    # Khung UI
    create_diagram_box(draw, 100, 100, 1000, 110, "TẦNG GIAO DIỆN (FRONTEND - WEB CLIENT)", "HTML5 / CSS3 Responsive / JavaScript / Chart.js / Multi-step Stepper", (239, 246, 255), (37, 99, 235))

    # Khung API
    create_diagram_box(draw, 100, 260, 1000, 100, "TẦNG RESTFUL API & SERVICES (BACKEND FASTAPI)", "Career Routes • Consultation Routes • History Routes • Admin & Auth Routes", (245, 243, 255), (124, 58, 237))

    # Khung Lõi Hệ Chuyên Gia
    draw.rectangle([100, 410, 1100, 580], fill=(240, 253, 244), outline=(16, 185, 129), width=3)
    draw.text((w // 2, 435), "LÕI HỆ CHUYÊN GIA (EXPERT SYSTEM CORE ENGINE)", fill=(6, 95, 70), anchor="mm", font=get_font(22))

    create_diagram_box(draw, 130, 470, 210, 85, "1. Facts Module", "Working Memory", (255, 255, 255), (16, 185, 129))
    create_diagram_box(draw, 370, 470, 210, 85, "2. Knowledge Base", "35+ IF-THEN Rules", (255, 255, 255), (16, 185, 129))
    create_diagram_box(draw, 610, 470, 210, 85, "3. Inference Engine", "Forward Chaining", (255, 255, 255), (16, 185, 129))
    create_diagram_box(draw, 850, 470, 220, 85, "4. Conflict & Trace", "Ranking & Explanation", (255, 255, 255), (16, 185, 129))

    # Khung Cơ sở dữ liệu
    create_diagram_box(draw, 100, 620, 1000, 90, "TẦNG CƠ SỞ DỮ LIỆU & LƯU TRỮ TRI THỨC (DATABASE / STORAGE)", "SQLite Database (Users, Students, Consultations) • JSON Knowledge Base (rules.json, fact_conventions.json)", (254, 243, 199), (217, 119, 6))

    # Mũi tên kết nối
    create_arrow(draw, (w // 2, 210), (w // 2, 260))
    create_arrow(draw, (w // 2, 360), (w // 2, 410))
    create_arrow(draw, (w // 2, 580), (w // 2, 620))

    img.save(REPORT_DIAG_DIR / "system_architecture.png", "PNG")
    print("Created system_architecture.png")


def create_use_case():
    """Tạo diagrams/use_case.png."""
    w, h = 1000, 650
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.text((w // 2, 40), "SƠ ĐỒ USE CASE HỆ THỐNG TƯ VẤN HƯỚNG NGHIỆP", fill=(15, 23, 42), anchor="mm", font=get_font(26))

    # Actor Học sinh
    draw.ellipse([80, 200, 160, 280], fill=(219, 234, 254), outline=(37, 99, 235), width=3)
    draw.text((120, 310), "Học sinh THPT", fill=(15, 23, 42), anchor="mm", font=get_font(18))

    # Actor Admin
    draw.ellipse([840, 200, 920, 280], fill=(254, 226, 226), outline=(220, 38, 38), width=3)
    draw.text((880, 310), "Quản trị viên (Admin)", fill=(15, 23, 42), anchor="mm", font=get_font(18))

    # Use cases
    cases = [
        (350, 110, "Làm bài trắc nghiệm RIASEC"),
        (350, 190, "Khai báo điểm học bạ 8 môn"),
        (350, 270, "Xem kết quả tư vấn & Radar Chart"),
        (350, 350, "Tra cứu danh mục ngành & khối thi"),
        (350, 430, "Xem vết suy diễn giải thích logic"),
        (350, 510, "Quản lý cơ sở tri thức (Bật/Tắt luật)"),
        (350, 580, "Xem thống kê lưu lượng hệ thống"),
    ]

    for idx, (x, y, text) in enumerate(cases):
        draw.rounded_rectangle([x, y, x + 300, y + 50], radius=15, fill=(241, 245, 249), outline=(100, 116, 139), width=2)
        draw.text((x + 150, y + 25), text, fill=(30, 41, 59), anchor="mm", font=get_font(15))
        if idx < 5:
            create_arrow(draw, (160, 240), (x, y + 25), color=(37, 99, 235), width=2)
        if idx >= 4:
            create_arrow(draw, (840, 240), (x + 300, y + 25), color=(220, 38, 38), width=2)

    img.save(REPORT_DIAG_DIR / "use_case.png", "PNG")
    print("Created use_case.png")


def create_activity_diagram():
    """Tạo diagrams/activity_diagram.png."""
    w, h = 900, 750
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.text((w // 2, 40), "SƠ ĐỒ HOẠT ĐỘNG (ACTIVITY DIAGRAM) SUY DIỄN TIẾN", fill=(15, 23, 42), anchor="mm", font=get_font(26))

    steps = [
        ("Bắt đầu: Học sinh gửi hồ sơ (Điểm + RIASEC)", (239, 246, 255), (37, 99, 235)),
        ("Khởi tạo Working Memory (Facts đầu vào)", (241, 245, 249), (100, 116, 139)),
        ("Tìm tập luật kích hoạt (Conflict Set thỏa mãn IF)", (254, 243, 199), (217, 119, 6)),
        ("Giải quyết xung đột (Chọn luật Confidence & Priority cao nhất)", (254, 226, 226), (220, 38, 38)),
        ("Bắn luật: Ghi nhận Fact trung gian hoặc Recommendation", (240, 253, 244), (16, 185, 129)),
        ("Kiểm tra điều kiện dừng (Hết luật thỏa mãn hoặc Fixed Point)", (245, 243, 255), (124, 58, 237)),
        ("Xếp hạng Top ngành phù hợp & Xuất vết giải thích (Trace)", (219, 234, 254), (37, 99, 235)),
    ]

    y_start = 90
    for idx, (title, fill, outline) in enumerate(steps):
        create_diagram_box(draw, 150, y_start, 600, 55, title, "", fill, outline)
        if idx < len(steps) - 1:
            create_arrow(draw, (450, y_start + 55), (450, y_start + 85))
        y_start += 85

    img.save(REPORT_DIAG_DIR / "activity_diagram.png", "PNG")
    print("Created activity_diagram.png")


def create_database_diagram():
    """Tạo diagrams/database_diagram.png (ERD)."""
    w, h = 1000, 680
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.text((w // 2, 40), "SƠ ĐỒ QUAN HỆ THỰC THỂ CƠ SỞ DỮ LIỆU (ERD)", fill=(15, 23, 42), anchor="mm", font=get_font(26))

    # USERS
    draw.rectangle([80, 100, 340, 260], fill=(239, 246, 255), outline=(37, 99, 235), width=2)
    draw.rectangle([80, 100, 340, 135], fill=(37, 99, 235))
    draw.text((210, 117), "USERS", fill=(255, 255, 255), anchor="mm", font=get_font(18))
    user_fields = ["PK id : VARCHAR(50)", "username : VARCHAR(50) [UQ]", "password_hash : VARCHAR(255)", "full_name : VARCHAR(150)", "email : VARCHAR(100)", "role : VARCHAR(20)"]
    for i, f in enumerate(user_fields):
        draw.text((95, 145 + i * 18), f, fill=(15, 23, 42), font=get_font(13))

    # STUDENTS
    draw.rectangle([80, 360, 340, 540], fill=(240, 253, 244), outline=(16, 185, 129), width=2)
    draw.rectangle([80, 360, 340, 395], fill=(16, 185, 129))
    draw.text((210, 377), "STUDENTS", fill=(255, 255, 255), anchor="mm", font=get_font(18))
    stu_fields = ["PK id : VARCHAR(50)", "FK user_id : VARCHAR(50)", "full_name : VARCHAR(150)", "grade : VARCHAR(10)", "school : VARCHAR(200)", "region : VARCHAR(50)", "track : VARCHAR(50)"]
    for i, f in enumerate(stu_fields):
        draw.text((95, 405 + i * 18), f, fill=(15, 23, 42), font=get_font(13))

    # CAREER_CATEGORIES
    draw.rectangle([660, 100, 920, 240], fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.rectangle([660, 100, 920, 135], fill=(217, 119, 6))
    draw.text((790, 117), "CAREER_CATEGORIES", fill=(255, 255, 255), anchor="mm", font=get_font(17))
    cat_fields = ["PK id : VARCHAR(50)", "name : VARCHAR(150)", "description : TEXT", "icon : VARCHAR(50)"]
    for i, f in enumerate(cat_fields):
        draw.text((675, 145 + i * 20), f, fill=(15, 23, 42), font=get_font(13))

    # CAREERS
    draw.rectangle([660, 340, 920, 580], fill=(245, 243, 255), outline=(124, 58, 237), width=2)
    draw.rectangle([660, 340, 920, 375], fill=(124, 58, 237))
    draw.text((790, 357), "CAREERS", fill=(255, 255, 255), anchor="mm", font=get_font(18))
    car_fields = ["PK id : VARCHAR(50)", "code : VARCHAR(50) [UQ]", "name : VARCHAR(200)", "FK category_id : VARCHAR(50)", "riasec_primary : CHAR(1)", "riasec_code : VARCHAR(10)", "required_blocks : TEXT", "average_salary : VARCHAR(100)", "market_trend : VARCHAR(100)"]
    for i, f in enumerate(car_fields):
        draw.text((675, 385 + i * 20), f, fill=(15, 23, 42), font=get_font(13))

    # CONSULTATIONS
    draw.rectangle([370, 240, 630, 480], fill=(254, 226, 226), outline=(220, 38, 38), width=2)
    draw.rectangle([370, 240, 630, 275], fill=(220, 38, 38))
    draw.text((500, 257), "CONSULTATIONS", fill=(255, 255, 255), anchor="mm", font=get_font(18))
    con_fields = ["PK id : VARCHAR(50)", "FK student_id : VARCHAR(50)", "FK user_id : VARCHAR(50)", "dominant_code : VARCHAR(10)", "scores_json : TEXT", "riasec_json : TEXT", "recommendations_json : TEXT", "explanation_json : TEXT"]
    for i, f in enumerate(con_fields):
        draw.text((385, 285 + i * 20), f, fill=(15, 23, 42), font=get_font(13))

    create_arrow(draw, (210, 260), (210, 360), color=(100, 116, 139))
    create_arrow(draw, (340, 420), (370, 360), color=(100, 116, 139))
    create_arrow(draw, (790, 240), (790, 340), color=(100, 116, 139))

    img.save(REPORT_DIAG_DIR / "database_diagram.png", "PNG")
    print("Created database_diagram.png")


if __name__ == "__main__":
    create_logo()
    create_banner()
    create_background()
    create_system_architecture()
    create_use_case()
    create_activity_diagram()
    create_database_diagram()
