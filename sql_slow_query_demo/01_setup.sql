DROP DATABASE IF EXISTS slow_query_demo;
CREATE DATABASE slow_query_demo CHARACTER SET utf8mb4;
USE slow_query_demo;

CREATE TABLE orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    order_no VARCHAR(32) NOT NULL,
    status VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    created_at DATETIME NOT NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB;

CREATE TABLE digits (n TINYINT PRIMARY KEY);
INSERT INTO digits VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8),(9);

INSERT INTO orders (user_id, order_no, status, amount, created_at)
SELECT
    IF(seq % 5 = 0, 10001, 20000 + seq % 10000),
    CONCAT('ORD', LPAD(seq, 10, '0')),
    CASE WHEN seq % 3 = 0 THEN 'PAID'
         WHEN seq % 3 = 1 THEN 'CREATED'
         ELSE 'CANCELLED' END,
    (seq % 50000) / 100 + 1,
    TIMESTAMP('2023-01-01 00:00:00') + INTERVAL (seq % 1200000) MINUTE
FROM (
    SELECT a.n + b.n*10 + c.n*100 + d.n*1000 + e.n*10000 + f.n*100000 AS seq
    FROM digits a CROSS JOIN digits b CROSS JOIN digits c
    CROSS JOIN digits d CROSS JOIN digits e CROSS JOIN digits f
) numbers;

DROP TABLE digits;
ANALYZE TABLE orders;
SELECT COUNT(*) AS total_rows,
       SUM(user_id = 10001) AS target_user_rows
FROM orders;

