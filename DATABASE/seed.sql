-- Seed dữ liệu mẫu cho hệ thống
-- Tài khoản mặc định:
-- 1. admin (Mật khẩu: admin123, role: admin) - hash sha256: 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9
-- 2. hocsinh1 (Mật khẩu: user123, role: user) - hash sha256: e6c279f622cdd5122e0dc6071400a6e0eeb9e149a4073377f8342d4ecacdc240
INSERT OR IGNORE INTO users (id, username, password_hash, full_name, email, role) VALUES
('usr_admin_01', 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Quản Trị Viên Hệ Thống', 'admin@educareer.edu.vn', 'admin'),
('usr_demo_01', 'hocsinh1', 'e6c279f622cdd5122e0dc6071400a6e0eeb9e149a4073377f8342d4ecacdc240', 'Nguyễn Văn Minh', 'hocsinh1@gmail.com', 'user');

INSERT OR IGNORE INTO career_categories (id, name, description, icon) VALUES
('CNTT', 'Công nghệ Thông tin', 'Lĩnh vực phần mềm, dữ liệu, trí tuệ nhân tạo và mạng máy tính', 'fa-laptop-code'),
('YDUOC', 'Y Dược & Chăm sóc Sức khỏe', 'Y khoa, dược học, điều dưỡng và chăm sóc sức khỏe cộng đồng', 'fa-user-md'),
('KINHTE', 'Kinh tế, Marketing & Quản lý', 'Quản trị kinh doanh, marketing số, logistics và tài chính', 'fa-chart-line'),
('NGHETHUAT', 'Nghệ thuật & Sáng tạo', 'Thiết kế đồ họa, mỹ thuật đa phương tiện và kiến trúc', 'fa-palette'),
('KYTHUAT', 'Kỹ thuật & Công nghệ', 'Tự động hóa, robot, điện tử và chế tạo máy', 'fa-robot'),
('GIAODUC', 'Giáo dục & Xã hội', 'Sư phạm, tâm lý học và quản lý giáo dục', 'fa-chalkboard-teacher');
