# tes1
# import sys
# if sys.platform == "win32":
#     sys.stdout.reconfigure(encoding="utf-8")
#     sys.stderr.reconfigure(encoding="utf-8")
# print("你好，世界 👋")

# tes2
# import re
# import time
# def _typewriter_print(text: str, delay_per_char: float = 0.03) -> None:
#     """逐字符打印 + 小延迟，把"几字一 chunk"匀成"一字一吐"的打字机节奏。
#     DeepSeek 的 stream chunk 一次常常吐 2-4 个汉字，业务解读又只有 70 字左右，
#     1.3 秒就吐完肉眼难察觉；按字节流后总耗时约 3 秒，正好和人的阅读速度对齐。"""
#     for ch in text:
#         print(ch, end="", flush=True)
#         time.sleep(delay_per_char)


# # 中文话术 trigger：只在出现这些词 / 标点时，才把"以中文开头的行"判定为
# # 解释性段落起点。Day 7-8 引入白名单模式，修复 D9-11：原版"任何中文行都截"
# # 的启发式会把主 SELECT 后的中文别名字段列表（如 "  月份," / "  月销售额,"）
# # 误判为话术，把整段 SQL 砍掉。
# _PROSE_LINE_TRIGGER = re.compile(
#     "[。！？：；]|"
#     "根据|首先|然后|接下来|现在|因此|所以|"
#     "这条|这个|这是|这就|这里|上面|下面|上述|由于|"
#     "等等|不过|另外|需要|应该|修正|重新|"
#     "注意|说明|解释|总结|综上|至此|完成|"
#     "让我|思考|分析|理解|意图|查询会|查询的|建议|推荐"
# )

# if __name__ == "__main__":
#     _typewriter_print("你好，\n世界！")
#     # print(type(_PROSE_LINE_TRIGGER))

# #tes3
# import re

# _PROSE_LINE_TRIGGER = re.compile(
#     "[。！？：；]|"
#     "根据|首先|然后|接下来|现在|因此|所以|"
#     "这条|这个|这是|这就|这里|上面|下面|上述|由于|"
#     "等等|不过|另外|需要|应该|修正|重新|"
#     "注意|说明|解释|总结|综上|至此|完成|"
#     "让我|思考|分析|理解|意图|查询会|查询的|建议|推荐"
# )

# def _strip_code_fence(text: str) -> str:
#     """从 LLM 输出里抽出干净 SQL。

#     需要处理三类噪声：
#       1. markdown 围栏 ```sql ... ```（Day 1-3 已有）
#       2. tool calling 后续轮，LLM 偶尔会在 SQL 前吐一句中文开场白
#          ("现在可以生成 SQL 了。") —— 用 SELECT/WITH/INSERT/UPDATE/DELETE/PRAGMA
#          关键字定位真实 SQL 起点，切掉前置话术
#       3. tool calling 后续轮，LLM 偶尔在给完一段 SQL 后又自言自语
#          ("等等，总金额需要...") 再贴一段二次 SQL —— 用结束围栏 ``` 或
#          "含明显话术 trigger 词的中文行" 作为 SQL 终点

#     Day 7-8 修复（D9-11 根因）：第 4 步从"任何中文行都当终点"改为白名单
#     trigger 词判定。中文字段别名（`月份,` `月销售额,`）一律保留，只有
#     含"根据/这条/等等/注意/。/！/？" 等明显话术信号的中文行才视为终点。
#     """
#     text = text.strip()
#     # 1) 整体剥首尾围栏
#     if text.startswith("```"):
#         text = re.sub(r"^```(?:sql)?\s*", "", text)
#         text = re.sub(r"\s*```$", "", text)
#         text = text.strip()
#     # 2) 截到第一个 SQL 关键字
#     m = re.search(r"(?is)\b(SELECT|WITH|INSERT|UPDATE|DELETE|PRAGMA)\b", text)
#     if m:
#         text = text[m.start():]
#     # 3) 截掉 SQL 后面跟的 ``` 围栏（含其后任何二次胡话）
#     fence_pos = text.find("```")
#     if fence_pos != -1:
#         text = text[:fence_pos]
#     # 4) 中文话术段落截断：只在行内含明显话术 trigger 时才截
#     lines = text.splitlines()
#     cut = len(lines)
#     for i, ln in enumerate(lines):
#         stripped = ln.strip()
#         if not stripped:
#             continue
#         first = stripped[0]
#         if not ("一" <= first <= "鿿"):
#             continue
#         if _PROSE_LINE_TRIGGER.search(stripped):
#             cut = i
#             break
#     text = "\n".join(lines[:cut])
#     return text.strip().rstrip(";").strip()

# if __name__ == "__main__":
#     print(_strip_code_fence(
#         "123 "
#     ))

# tes4

# import argparse

# parser = argparse.ArgumentParser(
#     description="SAP Smart Query Assistant - CLI Demo",
#     formatter_class=argparse.RawDescriptionHelpFormatter,
# )

# parser.add_argument("--query",  help="输入查询问题，例如：查询本月销售额")
# parser.add_argument("--table",  help="指定查询的表名，例如：VBAK")
# parser.add_argument("--limit",  type=int, default=10, help="返回行数，默认10")
# parser.add_argument("--verbose", action="store_true", help="显示详细信息")
# # args = parser.parse_args()  

# if __name__ == "__main__":
#     args = parser.parse_args()
#     if not args.query:
#         parser.print_help()
#     else:
#         if args.verbose:
#             print(f"[详细模式] 表: {args.table}, 行数限制: {args.limit}")
#         print(f"查询问题: {args.query}")
#         print(f"目标表:   {args.table or '未指定'}")
#         print(f"返回行数: {args.limit}")

# tes5
from pathlib import Path
from dotenv import load_dotenv
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
print(ROOT)


