import re


_PROSE_LINE_TRIGGER = re.compile(
    "[。！？：；]|"
    "根据|首先|然后|接下来|现在|因此|所以|"
    "这条|这个|这是|这就|这里|上面|下面|上述|由于|"
    "等等|不过|另外|需要|应该|修正|重新|"
    "注意|说明|解释|总结|综上|至此|完成|"
    "让我|思考|分析|理解|意图|查询会|查询的|建议|推荐"
)

def _strip_code_fence(text: str) -> str:
    """从 LLM 输出里抽出干净 SQL。

    需要处理三类噪声：
      1. markdown 围栏 ```sql ... ```（Day 1-3 已有）
      2. tool calling 后续轮，LLM 偶尔会在 SQL 前吐一句中文开场白
         ("现在可以生成 SQL 了。") —— 用 SELECT/WITH/INSERT/UPDATE/DELETE/PRAGMA
         关键字定位真实 SQL 起点，切掉前置话术
      3. tool calling 后续轮，LLM 偶尔在给完一段 SQL 后又自言自语
         ("等等，总金额需要...") 再贴一段二次 SQL —— 用结束围栏 ``` 或
         "含明显话术 trigger 词的中文行" 作为 SQL 终点

    Day 7-8 修复（D9-11 根因）：第 4 步从"任何中文行都当终点"改为白名单
    trigger 词判定。中文字段别名（`月份,` `月销售额,`）一律保留，只有
    含"根据/这条/等等/注意/。/！/？" 等明显话术信号的中文行才视为终点。
    """
    text = text.strip()
    # 1) 整体剥首尾围栏
    if text.startswith("```"):
        text = re.sub(r"^```(?:sql)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()
    # 2) 截到第一个 SQL 关键字
    m = re.search(r"(?is)\b(SELECT|WITH|INSERT|UPDATE|DELETE|PRAGMA)\b", text)
    if m:
        text = text[m.start():]
    # 3) 截掉 SQL 后面跟的 ``` 围栏（含其后任何二次胡话）
    fence_pos = text.find("```")
    if fence_pos != -1:
        text = text[:fence_pos]
    # 4) 中文话术段落截断：只在行内含明显话术 trigger 时才截
    lines = text.splitlines()
    cut = len(lines)
    for i, ln in enumerate(lines):
        stripped = ln.strip()
        if not stripped:
            continue
        first = stripped[0]
        if not ("一" <= first <= "鿿"):
            continue
        if _PROSE_LINE_TRIGGER.search(stripped):
            cut = i
            break
    text = "\n".join(lines[:cut])
    return text.strip().rstrip(";").strip()


if __name__ == "__main__":
    # 模拟 LLM 的真实输出：前面有说明，中间是 SQL，后面又跟了一段解释。
    mock_llm_output = """现在可以生成 SQL 了：
```sql
WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(created_at, '%Y-%m') AS 月份,
        COUNT(*) AS 订单数量,
        SUM(amount) AS 月销售额
    FROM orders
    WHERE status = 'PAID'
      AND created_at >= '2023-01-01'
      AND created_at < '2024-01-01'
    GROUP BY DATE_FORMAT(created_at, '%Y-%m')
)
SELECT 月份, 订单数量, 月销售额
FROM monthly_sales
ORDER BY 月份;
```
注意：这里使用 CTE 汇总每个月已支付订单的销售额。
"""

    expected_sql = """WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(created_at, '%Y-%m') AS 月份,
        COUNT(*) AS 订单数量,
        SUM(amount) AS 月销售额
    FROM orders
    WHERE status = 'PAID'
      AND created_at >= '2023-01-01'
      AND created_at < '2024-01-01'
    GROUP BY DATE_FORMAT(created_at, '%Y-%m')
)
SELECT 月份, 订单数量, 月销售额
FROM monthly_sales
ORDER BY 月份"""

    print("=== 清洗前的 SQL ===")
    print(mock_llm_output)
    cleaned_sql = _strip_code_fence(mock_llm_output)
    print("=== 清洗后的 SQL ===")
    print(cleaned_sql)
    assert cleaned_sql == expected_sql
    print("\n测试通过：前置说明、代码围栏和后置解释均已移除。")
