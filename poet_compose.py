import sys, torch
import torch.nn as nn
import torch.nn.functional as F
import zhconv   # 繁体 -> 简体
sys.stdout.reconfigure(encoding="utf-8")

# 必须和 train_poet.py 用完全相同的词表与配置
text = open("poems_data.txt", encoding="utf-8").read()
chars = sorted(set(text)); V = len(chars)
stoi = {c:i for i,c in enumerate(chars)}; itos = {i:c for i,c in enumerate(chars)}
enc = lambda s:[stoi[c] for c in s]; dec = lambda l:"".join(itos[i] for i in l)
BLOCK_SIZE, EMBED_DIM, N_HEADS, N_LAYERS, DROPOUT = 48, 192, 6, 5, 0.1
THEMES = ["春天","爱情","思乡","送别","月夜","山水","花","秋","雪","边塞"]

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
        if any(c not in stoi for c in theme):
            return "（这个主题里有训练数据没出现的字，换一个吧）"
        idx = torch.tensor([enc(f"【{theme}】")], dtype=torch.long)
        for _ in range(40):
            lg = s(idx[:,-BLOCK_SIZE:])[:,-1,:]/temp
            v,_ = torch.topk(lg, topk); lg[lg < v[:,[-1]]] = -float("inf")
            nx = torch.multinomial(F.softmax(lg,dim=-1),1)
            if itos[nx.item()] == "\n": break
            idx = torch.cat([idx,nx],dim=1)
        out = dec(idx[0].tolist())
        body = out.split("】",1)[1] if "】" in out else out
        return zhconv.convert(body, "zh-cn")

m = Poet(); m.load_state_dict(torch.load("poet.pth")); m.eval()
print("唐诗作诗机已就绪！")
print("内置主题：" + "、".join(THEMES))
print("（也可以试别的字，但训练数据里有的主题效果最好）\n")
while True:
    th = input("想写什么主题的诗？(输入 q 退出): ").strip()
    if th in ("q","quit","exit",""):
        print("再见！"); break
    print(f"\n《{th}》(AI作)")
    for i in range(3):   # 每个主题作 3 首，挑你喜欢的
        print(f"  {i+1}. {m.write(th)}")
    print()
