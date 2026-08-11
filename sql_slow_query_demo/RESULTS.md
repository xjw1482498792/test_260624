# 实测结果（MySQL 8.4.9）

测试数据：1,000,000 条订单，其中目标用户 200,000 条。

## 优化前

SQL 对 `created_at` 使用 `DATE()`，查询 2023 年 1 月的历史订单。

```text
Index scan on orders using idx_created_at (reverse)
actual time=0.0757..1763 rows=955660
Limit actual time=1846..1847 rows=20
```

为了找到历史月份中符合用户和状态条件的最新 20 条记录，MySQL 从时间
索引尾部反向扫描了 955,660 条记录，总耗时约 1,847 ms。

## 优化后

时间条件改写为左闭右开范围，并增加联合索引：

```sql
CREATE INDEX idx_user_status_created
ON orders(user_id, status, created_at DESC);
```

实测执行计划：

```text
Index range scan on orders using idx_user_status_created
actual time=6.05..6.05 rows=20
Limit actual time=6.05..6.06 rows=20
```

查询耗时从约 1,847 ms 降至约 6.06 ms，约提升 305 倍。单次结果会受到
缓存和机器负载影响，但扫描方式和数量级差异具有可重复性。
