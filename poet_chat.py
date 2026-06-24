import sys, random, torch
import torch.nn as nn
import torch.nn.functional as F
import zhconv   # 繁体 -> 简体
sys.stdout.reconfigure(encoding="utf-8")
try:
    sys.stdin.reconfigure(encoding="utf-8")   # 读入中文也要 UTF-8，否则关键词匹配失败
except Exception:
    pass

text = open("poems_data.txt", encoding="utf-8").read()
chars = sorted(set(text)); V = len(chars)
stoi = {c:i for i,c in enumerate(chars)}; itos = {i:c for i,c in enumerate(chars)}
enc = lambda s:[stoi[c] for c in s]; dec = lambda l:"".join(itos[i] for i in l)
BLOCK_SIZE, EMBED_DIM, N_HEADS, N_LAYERS, DROPOUT = 48, 192, 6, 5, 0.1

# 把用户的大白话映射到模型学过的 10 个主题
THEME_KEYWORDS = {
    "春天": ["春", "花开", "万物", "复苏"],
    "爱情": ["爱", "情", "想你", "喜欢", "相思", "恋", "心动", "思念", "美人", "她"],
    "思乡": ["家", "想家", "思乡", "故乡", "家乡", "漂泊", "游子", "回家"],
    "送别": ["别", "离别", "送别", "再见", "分别", "走了", "送你", "离开"],
    "月夜": ["月", "夜", "晚上", "夜晚", "失眠", "月亮"],
    "山水": ["山", "水", "江", "河", "风景", "旅行", "自然"],
    "花": ["花", "牡丹", "桃花", "梅"],
    "秋": ["秋", "落叶", "秋天"],
    "雪": ["雪", "冬", "冬天", "寒冷"],
    "边塞": ["边塞", "战", "塞外", "打仗", "将军", "沙场", "出征"],
}

def detect_theme(s):
    for theme, kws in THEME_KEYWORDS.items():
        if theme in s or any(k in s for k in kws):
            return theme
    return None

class Head(nn.Module):
    def __init__(s,h):
        super().__init__(); s.q=nn.Linear(EMBED_DIM,h,bias=False); s.k=nn.Linear(EMBED_DIM,h,bias=False); s.v=nn.Linear(EMBED_DIM,h,bias=False)
        s.register_buffer("m",torch.tril(torch.ones(BLOCK_SIZE,BLOCK_SIZE))); s.d=nn.Dropout(DROPOUT)
    def forward(s,x):
        B,T,C=x.shape; a=s.q(x)@s.k(x).transpose(-2,-1)*s.k(x).shape[-1]**-0.5
        a=s.d(F.softmax(a.masked_fill(s.m[:T,:T]==0,float("-inf")),dim=-1)); return a@s.v(x)
class MH(nn.Module):
    def __init__(s,n,h):
        super().__init__(); s.h=nn.ModuleList([Head(h) for _ in range(n)]); s.p=nn.Linear(EMBED_DIM,EMBED_DIM); s.d=nn.Dropout(DROPOUT)
    def forward(s,x): return s.d(s.p(torch.cat([h(x) for h in s.h],dim=-1)))
class FFN(nn.Module):
    def __init__(s): super().__init__(); s.n=nn.Sequential(nn.Linear(EMBED_DIM,4*EMBED_DIM),nn.ReLU(),nn.Linear(4*EMBED_DIM,EMBED_DIM),nn.Dropout(DROPOUT))
    def forward(s,x): return s.n(x)
class Blk(nn.Module):
    def __init__(s):
        super().__init__(); s.a=MH(N_HEADS,EMBED_DIM//N_HEADS); s.f=FFN(); s.l1=nn.LayerNorm(EMBED_DIM); s.l2=nn.LayerNorm(EMBED_DIM)
    def forward(s,x): x=x+s.a(s.l1(x)); return x+s.f(s.l2(x))
class Poet(nn.Module):
    def __init__(s):
        super().__init__(); s.te=nn.Embedding(V,EMBED_DIM); s.pe=nn.Embedding(BLOCK_SIZE,EMBED_DIM)
        s.b=nn.Sequential(*[Blk() for _ in range(N_LAYERS)]); s.lf=nn.LayerNorm(EMBED_DIM); s.hd=nn.Linear(EMBED_DIM,V)
    def forward(s,idx):
        B,T=idx.shape; x=s.te(idx)+s.pe(torch.arange(T)); x=s.lf(s.b(x)); return s.hd(x)
    @torch.no_grad()
    def write(s, theme, temp=0.85, topk=20):
        idx = torch.tensor([enc(f"【{theme}】")], dtype=torch.long)
        for _ in range(40):
            lg = s(idx[:,-BLOCK_SIZE:])[:,-1,:]/temp
            v,_ = torch.topk(lg, topk); lg[lg < v[:,[-1]]] = -float("inf")
            nx = torch.multinomial(F.softmax(lg,dim=-1),1)
            if itos[nx.item()] == "\n": break
            idx = torch.cat([idx,nx],dim=1)
        return zhconv.convert(dec(idx[0].tolist()).split("】",1)[1], "zh-cn")

m = Poet(); m.load_state_dict(torch.load("poet.pth")); m.eval()

print("🪶 小诗（AI诗人）已上线。")
print("跟我聊聊你的心情或想要的主题，我就写首诗给你。比如：")
print("  「我有点想家了」「写首关于爱情的」「下雪了」")
print("（输入 q 结束）\n")

GREET = ["好，听你这么说，我写了一首：", "有了，请看：", "这首送给你：", "我想到几句："]
while True:
    s = input("你：").strip()
    if s in ("q","quit","exit",""):
        print("小诗：青山不改，绿水长流，后会有期。"); break
    theme = detect_theme(s)
    if theme is None:
        theme = random.choice(["春天","爱情","思乡","月夜"])
        print(f"小诗：我没太听出主题，就凭感觉写一首『{theme}』吧——")
    else:
        print(f"小诗：{random.choice(GREET)}（{theme}）")
    print(f"      {m.write(theme)}\n")
