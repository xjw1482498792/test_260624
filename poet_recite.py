import sys, torch
import torch.nn as nn
import torch.nn.functional as F
import zhconv
sys.stdout.reconfigure(encoding="utf-8")
try: sys.stdin.reconfigure(encoding="utf-8")
except Exception: pass

text = open("poems_data.txt", encoding="utf-8").read()
chars = sorted(set(text)); V = len(chars)
stoi = {c:i for i,c in enumerate(chars)}; itos = {i:c for i,c in enumerate(chars)}
enc = lambda s:[stoi[c] for c in s]; dec = lambda l:"".join(itos[i] for i in l)
BLOCK_SIZE, EMBED_DIM, N_HEADS, N_LAYERS, DROPOUT = 48, 192, 6, 5, 0.1

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
    def cont(s, seed, temp=0.6, topk=10):   # 低温度 -> 更倾向“按记忆背诵”而非自由发挥
        if any(c not in stoi for c in seed):
            return "（开头里有训练数据没出现的字，换一句吧）"
        idx = torch.tensor([enc(seed)], dtype=torch.long)
        for _ in range(40):
            lg = s(idx[:,-BLOCK_SIZE:])[:,-1,:]/temp
            v,_ = torch.topk(lg, topk); lg[lg < v[:,[-1]]] = -float("inf")
            nx = torch.multinomial(F.softmax(lg,dim=-1),1)
            if itos[nx.item()] == "\n": break
            idx = torch.cat([idx,nx],dim=1)
        return zhconv.convert(dec(idx[0].tolist()), "zh-cn")

m = Poet(); m.load_state_dict(torch.load("poet.pth")); m.eval()

# 用几句名篇开头测试它能不能“背”出下文（繁体喂入，因为它内部是繁体）
tests = ["春眠不覺曉", "牀前明月光", "白日依山盡", "千山鳥飛絕", "勸君更盡一杯酒"]
print("给开头，看它能不能接出全诗：\n")
for seed in tests:
    print(f"  我给：{zhconv.convert(seed,'zh-cn')}…")
    print(f"  它接：{m.cont(seed)}\n")

print("="*40)
print("你也可以自己给开头让它接（输入 q 退出）：")
while True:
    seed = input("开头：").strip()
    if seed in ("q","quit","exit",""): break
    # 用户可能输简体，转成繁体再喂给模型
    print(f"它接：{m.cont(zhconv.convert(seed,'zh-hant'))}\n")
