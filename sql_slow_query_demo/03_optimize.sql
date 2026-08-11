USE slow_query_demo;

ALTER TABLE orders
    ADD INDEX idx_user_status_created (user_id, status, created_at DESC);
ANALYZE TABLE orders;

EXPLAIN ANALYZE
SELECT id, order_no, amount, status, created_at
FROM orders
WHERE user_id = 10001
  AND status = 'PAID'
  AND created_at >= '2023-01-01 00:00:00'
  AND created_at <  '2023-02-01 00:00:00'
ORDER BY created_at DESC
LIMIT 20;
