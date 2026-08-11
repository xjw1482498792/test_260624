# MySQL 慢查询优化演示

案例包含三个脚本：

1. `01_setup.sql`：创建演示库并生成 100 万条订单。
2. `02_before.sql`：执行优化前 SQL 和 `EXPLAIN ANALYZE`。
3. `03_optimize.sql`：添加联合索引、改写 SQL，再次执行分析。

核心优化：去掉索引列上的 `DATE()`、按查询模式建立
`(user_id, status, created_at DESC)` 联合索引，并避免 `SELECT *`。

本机实测数据见 `RESULTS.md`。
