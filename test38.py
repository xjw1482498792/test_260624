from decimal import Decimal

import pymysql


DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "demo_user",
    "password": "Demo@MySQL2026!",
    "database": "shop",
    "charset": "utf8mb4",
}

BATCH_SIZE = 3


connection = pymysql.connect(**DB_CONFIG)

try:
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE order_result")

    last_id = 0
    batch_number = 0

    while True:
        # 每次 SQL 最多只从数据库读取 BATCH_SIZE 条，不会一次取出全部数据。
        with connection.cursor() as read_cursor:
            read_cursor.execute(
                """
                SELECT id, customer_name, amount
                FROM orders
                WHERE id > %s
                ORDER BY id
                LIMIT %s
                """,
                (last_id, BATCH_SIZE),
            )
            rows = read_cursor.fetchall()

        if not rows:
            break

        batch_number += 1
        results = []

        for order_id, customer_name, amount in rows:
            tax_amount = amount * Decimal("1.13")
            results.append((order_id, tax_amount))
            print(
                f"  订单 {order_id}: {customer_name}, "
                f"未税 {amount:.2f}, 含税 {tax_amount:.2f}"
            )

        with connection.cursor() as write_cursor:
            write_cursor.executemany(
                """
                INSERT INTO order_result(order_id, tax_amount)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE tax_amount = VALUES(tax_amount)
                """,
                results,
            )

        connection.commit()
        last_id = rows[-1][0]
        print(
            f"第 {batch_number} 批处理完成：{len(rows)} 条，"
            f"当前 last_id={last_id}\n"
        )

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM order_result")
        total = cursor.fetchone()[0]
        print(f"全部处理完成，共写入 {total} 条结果。")
finally:
    connection.close()
