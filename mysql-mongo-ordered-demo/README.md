# MySQL -> MongoDB 有序同步演示

题目目标：4 个业务都读取同一张 MySQL 表的千万级数据，经过各自的业务处理后写入各自的 MongoDB 集合，并保持 MySQL 自增 ID 的顺序。

## 方案

```text
MySQL（一次游标分页读取）
              |
              +--> 业务 A 写入链：page1 -> page2 -> page3 -> Mongo A
              +--> 业务 B 写入链：page1 -> page2 -> page3 -> Mongo B
              +--> 业务 C 写入链：page1 -> page2 -> page3 -> Mongo C
              +--> 业务 D 写入链：page1 -> page2 -> page3 -> Mongo D
```

- 用策略模式封装 4 个业务的差异，公共的分页、并发、限流和异常处理只写一次。
- MySQL 使用 Keyset Pagination：`where id > ? order by id limit ?`，不使用千万级数据下越来越慢的 `offset`。
- MySQL 每页只查询一次，同一页交给 4 个业务并行处理。
- 每个业务维护一条 `CompletableFuture` 写入链。因此同一集合永远是第 N 页写完后才写第 N+1 页；4 个集合之间仍然并行。
- 用 `Semaphore` 限制在途页数，形成背压，避免把 1000 万行堆进 JVM。
- MongoDB 文档用 MySQL ID 作为 `_id`。批量写入使用 `ordered(true)`；读取结果时仍必须显式 `sort({_id: 1})`，因为 MongoDB 不保证无排序查询的自然顺序。

## 直接演示

演示程序不依赖 MySQL、MongoDB 或第三方 jar，而是使用内存适配器模拟两端。它会生成含 ID 空洞的数据，以证明代码没有错误地假设 ID 连续。

要求 JDK 8+（需要 `javac`，只有 JRE 不够）：

```powershell
cd mysql-mongo-ordered-demo
.\run.ps1
```

也可手动执行：

```powershell
javac -encoding UTF-8 -d out src\OrderedSyncDemo.java
java -cp out OrderedSyncDemo
```

预期会看到 4 个业务交错执行，但最终每个集合都输出 `ordered=true`。

## 替换为真实数据库

演示中的两个接口就是适配边界：

```java
interface MysqlSource {
    List<SourceRow> findNext(long lastId, int limit) throws Exception;
}

interface MongoSink {
    void writeOrdered(String collection, List<Document> documents) throws Exception;
}
```

真实 MySQL 查询应保持以下形式，并在单独的只读事务/一致性快照中执行：

```java
String sql = "select id, name, amount from source_order " +
             "where id > ? and id <= ? order by id asc limit ?";
```

同步开始时先取得 `max(id)` 作为本次任务的 `upperBound`。增加 `id <= upperBound` 后，本次同步不会不断追逐同步期间新增的数据。若要求严格一致性，可以用 MySQL `REPEATABLE READ` 一致性快照，或者使用 CDC（如 Debezium）承接快照之后的增量。

真实 MongoDB Java Driver 的核心写法：

```java
List<WriteModel<org.bson.Document>> writes = documents.stream()
    .map(d -> new ReplaceOneModel<>(
        Filters.eq("_id", d.id),
        new org.bson.Document("_id", d.id)
            .append("name", d.name)
            .append("result", d.result),
        new ReplaceOptions().upsert(true)))
    .collect(Collectors.toList());

collection.bulkWrite(writes, new BulkWriteOptions().ordered(true));
```

`upsert + _id=MySQL_ID` 支持失败后安全重跑。若目标集合一定为空，追求极限吞吐量时可改用 `insertMany(documents, new InsertManyOptions().ordered(true))`。

## 生产参数建议

- `PAGE_SIZE` 从 2,000～10,000 压测，不要一次加载 1000 万行。
- `MAX_IN_FLIGHT_PAGES` 从 2～8 压测；过大只会提高内存和数据库压力。
- 在 MySQL 主键上分页，不做 `offset`。
- 每个 Mongo 集合只有一条逻辑写入链；不要让多个线程同时向同一集合写不同 ID 段后再依赖“自然顺序”。
- 记录每个业务最后成功的 ID 作为 checkpoint。演示用 `_id` upsert 保证重跑幂等，实际项目可同时保存 checkpoint 以减少重复扫描。

如果 4 个业务的筛选 SQL 并不相同，不能共享一次扫描，则仍复用同一个模板，给每个业务各自配置 `MysqlSource`，再并行启动 4 次同步即可；有序保证方法不变。
