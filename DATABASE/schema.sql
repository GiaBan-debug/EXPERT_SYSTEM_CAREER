-- Schema cơ sở dữ liệu Hệ chuyên gia tư vấn hướng nghiệp THPT
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE,
    role VARCHAR(20) NOT NULL DEFAULT 'user', -- 'admin' hoặc 'user'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS students (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    full_name VARCHAR(150) NOT NULL,
    grade VARCHAR(10) NOT NULL DEFAULT '12',
    school VARCHAR(200),
    region VARCHAR(50) DEFAULT 'south',
    track VARCHAR(50) DEFAULT 'khoa_hoc_tu_nhien',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS career_categories (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    icon VARCHAR(50) DEFAULT 'fa-folder'
);

CREATE TABLE IF NOT EXISTS careers (
    id VARCHAR(50) PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    category_id VARCHAR(50) NOT NULL,
    description TEXT,
    riasec_primary CHAR(1) NOT NULL,
    riasec_code VARCHAR(10) NOT NULL,
    required_blocks TEXT,
    top_universities TEXT,
    average_salary VARCHAR(100),
    market_trend VARCHAR(100),
    icon VARCHAR(50) DEFAULT 'fa-briefcase',
    FOREIGN KEY (category_id) REFERENCES career_categories(id)
);

CREATE TABLE IF NOT EXISTS consultations (
    id VARCHAR(50) PRIMARY KEY,
    student_id VARCHAR(50),
    user_id VARCHAR(50),
    dominant_code VARCHAR(10) NOT NULL,
    scores_json TEXT NOT NULL,
    riasec_json TEXT NOT NULL,
    preferences_json TEXT,
    recommendations_json TEXT NOT NULL,
    explanation_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS system_rules (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    conditions_json TEXT NOT NULL,
    conclusion_json TEXT NOT NULL,
    priority INT DEFAULT 5,
    confidence REAL DEFAULT 1.0,
    enabled BOOLEAN DEFAULT TRUE
);
