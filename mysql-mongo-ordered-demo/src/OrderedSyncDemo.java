import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.HashSet;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicLong;

/**
 * 零依赖演示：共享读取一次 MySQL 页面，4 个业务并行处理；
 * 同一业务通过 CompletableFuture 链严格按页面顺序写 MongoDB。
 */
public final class OrderedSyncDemo {
    private static final int DEMO_ROW_COUNT = 50_000;
    private static final int PAGE_SIZE = 2_000;
    private static final int MAX_IN_FLIGHT_PAGES = 4;

    public static void main(String[] args) throws Exception {
        List<SourceRow> mysqlRows = buildSourceRows(DEMO_ROW_COUNT);
        MysqlSource mysql = new InMemoryMysqlSource(mysqlRows);
        InMemoryMongoSink mongo = new InMemoryMongoSink();

        List<BusinessStrategy> businesses = Arrays.asList(
                new AuditBusiness(),
                new ReportBusiness(),
                new ArchiveBusiness(),
                new RiskBusiness()
        );

        long begin = System.currentTimeMillis();
        OrderedMigrationTemplate template = new OrderedMigrationTemplate(
                mysql, mongo, businesses, PAGE_SIZE, MAX_IN_FLIGHT_PAGES);
        MigrationResult result = template.execute();
        long elapsed = System.currentTimeMillis() - begin;

        System.out.println();
        System.out.println("===== 最终校验 =====");
        for (BusinessStrategy business : businesses) {
            List<TargetDocument> documents = mongo.findAllOrderById(business.collectionName());
            boolean ordered = isStrictlyOrdered(documents);
            if (documents.size() != mysqlRows.size() || !ordered) {
                throw new IllegalStateException("集合校验失败: " + business.collectionName());
            }
            System.out.printf("%-20s count=%d, firstId=%d, lastId=%d, ordered=%s%n",
                    business.collectionName(), documents.size(),
                    documents.get(0).id, documents.get(documents.size() - 1).id, ordered);
        }
        System.out.printf("MySQL 实际分页查询 %d 次（不是 4 倍），迁移 %d 行，耗时 %d ms%n",
                result.mysqlQueryCount, result.sourceRowCount, elapsed);
    }

    /** 公共同步模板：所有分页、流水线、背压和有序控制都集中在这里。 */
    static final class OrderedMigrationTemplate {
        private final MysqlSource mysql;
        private final MongoSink mongo;
        private final List<BusinessStrategy> businesses;
        private final int pageSize;
        private final Semaphore inFlightPages;
        private final ExecutorService writerPool;

        OrderedMigrationTemplate(MysqlSource mysql,
                                 MongoSink mongo,
                                 List<BusinessStrategy> businesses,
                                 int pageSize,
                                 int maxInFlightPages) {
            this.mysql = mysql;
            this.mongo = mongo;
            this.businesses = businesses;
            this.pageSize = pageSize;
            this.inFlightPages = new Semaphore(maxInFlightPages);
            this.writerPool = Executors.newFixedThreadPool(businesses.size());
        }

        MigrationResult execute() throws Exception {
            Map<String, CompletableFuture<Void>> tails = new LinkedHashMap<>();
            for (BusinessStrategy business : businesses) {
                tails.put(business.collectionName(), CompletableFuture.completedFuture(null));
            }

            long lastId = 0L;
            long sourceRowCount = 0L;
            long queryCount = 0L;
            int pageNo = 0;

            try {
                while (true) {
                    inFlightPages.acquire();
                    List<SourceRow> rows;
                    try {
                        rows = mysql.findNext(lastId, pageSize);
                        queryCount++;
                    } catch (Exception e) {
                        inFlightPages.release();
                        throw e;
                    }

                    if (rows.isEmpty()) {
                        inFlightPages.release();
                        break;
                    }

                    assertSourceOrder(rows, lastId);
                    pageNo++;
                    final int currentPage = pageNo;
                    final List<SourceRow> immutablePage = Collections.unmodifiableList(
                            new ArrayList<>(rows));
                    List<CompletableFuture<Void>> pageJobs = new ArrayList<>();

                    for (final BusinessStrategy business : businesses) {
                        CompletableFuture<Void> previous = tails.get(business.collectionName());
                        CompletableFuture<Void> next = previous.thenRunAsync(() -> {
                            try {
                                List<TargetDocument> documents = new ArrayList<>(immutablePage.size());
                                for (SourceRow row : immutablePage) {
                                    documents.add(business.convert(row));
                                }
                                mongo.writeOrdered(business.collectionName(), documents);
                                System.out.printf("page=%02d, business=%-8s, id=%d..%d, thread=%s%n",
                                        currentPage, business.name(),
                                        immutablePage.get(0).id,
                                        immutablePage.get(immutablePage.size() - 1).id,
                                        Thread.currentThread().getName());
                            } catch (Exception e) {
                                throw new CompletionException(e);
                            }
                        }, writerPool);
                        tails.put(business.collectionName(), next);
                        pageJobs.add(next);
                    }

                    CompletableFuture.allOf(pageJobs.toArray(new CompletableFuture[0]))
                            .whenComplete((ignored, error) -> inFlightPages.release());

                    sourceRowCount += rows.size();
                    lastId = rows.get(rows.size() - 1).id;
                }

                CompletableFuture.allOf(tails.values().toArray(new CompletableFuture[0])).join();
                return new MigrationResult(sourceRowCount, queryCount);
            } catch (CompletionException e) {
                Throwable cause = e.getCause() == null ? e : e.getCause();
                throw new Exception("MongoDB 写入流水线失败", cause);
            } finally {
                writerPool.shutdown();
                if (!writerPool.awaitTermination(30, TimeUnit.SECONDS)) {
                    writerPool.shutdownNow();
                }
            }
        }
    }

    /** 策略接口：新增业务只需新增实现，不复制迁移流程。 */
    interface BusinessStrategy {
        String name();
        String collectionName();
        TargetDocument convert(SourceRow row);
    }

    static final class AuditBusiness implements BusinessStrategy {
        public String name() { return "审计"; }
        public String collectionName() { return "audit_orders"; }
        public TargetDocument convert(SourceRow row) {
            return TargetDocument.of(row, "AUDIT:" + row.name);
        }
    }

    static final class ReportBusiness implements BusinessStrategy {
        public String name() { return "报表"; }
        public String collectionName() { return "report_orders"; }
        public TargetDocument convert(SourceRow row) {
            return TargetDocument.of(row, "REPORT_AMOUNT:" + row.amount);
        }
    }

    static final class ArchiveBusiness implements BusinessStrategy {
        public String name() { return "归档"; }
        public String collectionName() { return "archive_orders"; }
        public TargetDocument convert(SourceRow row) {
            return TargetDocument.of(row, "ARCHIVE:" + row.name.toLowerCase());
        }
    }

    static final class RiskBusiness implements BusinessStrategy {
        public String name() { return "风控"; }
        public String collectionName() { return "risk_orders"; }
        public TargetDocument convert(SourceRow row) {
            String level = row.amount.compareTo(new BigDecimal("5000")) >= 0 ? "HIGH" : "NORMAL";
            return TargetDocument.of(row, "RISK:" + level);
        }
    }

    interface MysqlSource {
        /** 等价于 where id > :lastId order by id asc limit :limit。 */
        List<SourceRow> findNext(long lastId, int limit) throws Exception;
    }

    interface MongoSink {
        /** 真实实现使用 bulkWrite/insertMany，并设置 ordered(true)。 */
        void writeOrdered(String collection, List<TargetDocument> documents) throws Exception;
    }

    static final class InMemoryMysqlSource implements MysqlSource {
        private final List<SourceRow> rows;
        private final AtomicLong queryCount = new AtomicLong();

        InMemoryMysqlSource(List<SourceRow> rows) {
            this.rows = rows;
        }

        public List<SourceRow> findNext(long lastId, int limit) {
            queryCount.incrementAndGet();
            int from = firstIndexGreaterThan(lastId);
            if (from >= rows.size()) {
                return Collections.emptyList();
            }
            int to = Math.min(from + limit, rows.size());
            return new ArrayList<>(rows.subList(from, to));
        }

        private int firstIndexGreaterThan(long id) {
            int low = 0;
            int high = rows.size();
            while (low < high) {
                int mid = (low + high) >>> 1;
                if (rows.get(mid).id <= id) {
                    low = mid + 1;
                } else {
                    high = mid;
                }
            }
            return low;
        }
    }

    static final class InMemoryMongoSink implements MongoSink {
        private final Map<String, List<TargetDocument>> collections = new ConcurrentHashMap<>();
        private final Map<String, Set<Long>> ids = new ConcurrentHashMap<>();

        public void writeOrdered(String collection, List<TargetDocument> documents) throws Exception {
            // 随机风格延迟用来制造线程交错，便于观察不同业务确实在并行。
            long delay = Math.abs(collection.hashCode() + documents.get(0).id) % 4L;
            Thread.sleep(delay);

            List<TargetDocument> target = collections.computeIfAbsent(
                    collection, key -> Collections.synchronizedList(new ArrayList<>()));
            Set<Long> knownIds = ids.computeIfAbsent(
                    collection, key -> Collections.synchronizedSet(new HashSet<>()));

            synchronized (target) {
                for (TargetDocument document : documents) {
                    // 模拟 MongoDB _id upsert：重跑不会生成重复文档。
                    if (knownIds.add(document.id)) {
                        target.add(document);
                    }
                }
            }
        }

        List<TargetDocument> findAllOrderById(String collection) {
            List<TargetDocument> result = new ArrayList<>(
                    collections.getOrDefault(collection, Collections.emptyList()));
            // 对应 MongoDB 查询中的 sort({_id: 1})。
            result.sort((left, right) -> Long.compare(left.id, right.id));
            return result;
        }
    }

    static final class SourceRow {
        final long id;
        final String name;
        final BigDecimal amount;

        SourceRow(long id, String name, BigDecimal amount) {
            this.id = id;
            this.name = name;
            this.amount = amount;
        }
    }

    static final class TargetDocument {
        final long id;       // 真实 MongoDB 中作为 _id
        final String name;
        final String result;

        TargetDocument(long id, String name, String result) {
            this.id = id;
            this.name = name;
            this.result = result;
        }

        static TargetDocument of(SourceRow row, String result) {
            return new TargetDocument(row.id, row.name, result);
        }
    }

    static final class MigrationResult {
        final long sourceRowCount;
        final long mysqlQueryCount;

        MigrationResult(long sourceRowCount, long mysqlQueryCount) {
            this.sourceRowCount = sourceRowCount;
            this.mysqlQueryCount = mysqlQueryCount;
        }
    }

    private static List<SourceRow> buildSourceRows(int count) {
        List<SourceRow> rows = new ArrayList<>(count);
        long id = 0L;
        for (int i = 1; i <= count; i++) {
            id++;
            if (i % 97 == 0) {
                id += 2; // 制造自增 ID 空洞，证明游标分页不要求 ID 连续。
            }
            rows.add(new SourceRow(id, "order-" + id,
                    BigDecimal.valueOf((id * 37L) % 10_000L)));
        }
        return rows;
    }

    private static void assertSourceOrder(List<SourceRow> rows, long previousLastId) {
        long last = previousLastId;
        for (SourceRow row : rows) {
            if (row.id <= last) {
                throw new IllegalStateException("MySQL 页面没有按 ID 严格升序");
            }
            last = row.id;
        }
    }

    private static boolean isStrictlyOrdered(List<TargetDocument> documents) {
        long last = Long.MIN_VALUE;
        for (TargetDocument document : documents) {
            if (document.id <= last) {
                return false;
            }
            last = document.id;
        }
        return true;
    }
}
