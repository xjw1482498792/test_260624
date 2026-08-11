USE slow_query_demo;

EXPLAIN ANALYZE
SELECT *
FROM orders
WHERE user_id = 10001
  AND status = 'PAID'
  AND DATE(created_at) >= '2023-01-01'
  AND DATE(created_at) <  '2023-02-01'
ORDER BY created_at DESC
LIMIT 20;
