import re


text = """```
        
       第一段回答。
       SELECT
       第二段回答。 
       ```
       ```
"""
print(f'before:{text}')

    # 1) 整体剥首尾围栏
if text.startswith("```"):
    text = re.sub(r"^```(?:sql)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()
    print(f'after 1):{text}')

# 2) 截到第一个 SQL 关键字
m = re.search(r"(?is)\b(SELECT|WITH|INSERT|UPDATE|DELETE|PRAGMA)\b", text)
if m:
    text = text[m.start():]    
    print(f'after 2):{text}')

# 3) 截掉 SQL 后面跟的 ``` 围栏（含其后任何二次胡话）
fence_pos = text.find("```")
if fence_pos != -1:
    text = text[:fence_pos]    
    print(f'after 3):{text}')    
 # 4) 中文话术段落截断：只在行内含明显话术 trigger 时才截
_PROSE_LINE_TRIGGER = re.compile(
    "[。！？：；]|"
    "根据|首先|然后|接下来|现在|因此|所以|"
    "这条|这个|这是|这就|这里|上面|下面|上述|由于|"
    "等等|不过|另外|需要|应该|修正|重新|"
    "注意|说明|解释|总结|综上|至此|完成|"
    "让我|思考|分析|理解|意图|查询会|查询的|建议|推荐"
) 
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
        match = _PROSE_LINE_TRIGGER.search(stripped)

        if match:
            print("整行：", repr(stripped))
            print("匹配内容：", repr(match.group()))
            print("匹配位置：", match.span())
        cut = i
        break
text = "\n".join(lines[:cut])
print(f'after 4):{text}')   