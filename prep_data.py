import sys, json, urllib.request
sys.stdout.reconfigure(encoding="utf-8")

# 主题 -> 关键词（繁体，因为数据是繁体）。按顺序匹配，取第一个命中的主题为主标签。
THEMES = [
    ("春天", ["春"]),
    ("爱情", ["情", "相思", "憶", "愛", "淚", "恨", "妾", "君"]),
    ("思乡", ["鄉", "故", "歸", "客", "家"]),
    ("送别", ["別", "送", "離", "贈"]),
    ("月夜", ["月", "夜"]),
    ("山水", ["山", "水", "江", "河", "湖"]),
    ("花", ["花"]),
    ("秋", ["秋"]),
    ("雪", ["雪"]),
    ("边塞", ["邊", "塞", "胡", "沙", "征", "戰", "關"]),
]

def theme_of(body):
    for name, kws in THEMES:
        if any(k in body for k in kws):
            return name
    return None

def is_quatrain(body):
    # 4 句、每句字数相等且为 5 或 7（五言/七言绝句）
    clauses = [c for c in body.replace("。", "，").split("，") if c]
    if len(clauses) != 4:
        return False
    L = len(clauses[0])
    return L in (5, 7) and all(len(c) == L for c in clauses)

collected = []
seen = set()
# chinese-poetry 全唐诗：poet.tang.0.json ~ poet.tang.57000.json，每个 1000 首
base = "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E5%85%A8%E5%94%90%E8%AF%97/poet.tang.{}.json"
for k in range(0, 20000, 1000):   # 下载 20 个文件 ≈ 2 万首，筛出绝句
    try:
        url = base.format(k)
        data = json.loads(urllib.request.urlopen(url, timeout=30).read().decode("utf-8"))
    except Exception as e:
        print(f"  跳过 {k}: {e}")
        continue
    for p in data:
        body = "".join(p.get("paragraphs", []))
        if not is_quatrain(body):
            continue
        th = theme_of(body)
        if th is None:
            continue
        if body in seen:
            continue
        seen.add(body)
        collected.append((th, body))
    print(f"  已处理到 poet.tang.{k}，累计绝句 {len(collected)} 首")

# 写出训练语料：每行 “【主题】正文”
with open("poems_data.txt", "w", encoding="utf-8") as f:
    for th, body in collected:
        f.write(f"【{th}】{body}\n")

print(f"\n完成！共收集 {len(collected)} 首绝句，写入 poems_data.txt")
from collections import Counter
cnt = Counter(th for th, _ in collected)
print("各主题数量：")
for th, n in cnt.most_common():
    print(f"  {th}: {n}")
print("\n示例：")
for th, body in collected[:5]:
    print(f"  【{th}】{body}")
