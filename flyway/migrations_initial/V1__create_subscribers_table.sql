-- V1__create_subscribers_table.sql
-- Initial schema: Create subscribers table

CREATE TABLE subscribers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data for testing
INSERT INTO subscribers (first_name, last_name, phone) VALUES
('John', 'Doe', '555-0001'),
('Jane', 'Smith', '555-0002'),
('Bob', 'Johnson', '555-0003');