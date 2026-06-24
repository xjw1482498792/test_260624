import sys, torch
import torch.nn as nn
import torch.nn.functional as F
sys.stdout.reconfigure(encoding="utf-8")

text = open("poems_data.txt", encoding="utf-8").read()
chars = sorted(set(text)); V = len(chars)
stoi = {c:i for i,c in enumerate(chars)}; itos = {i:c for i,c in enumerate(chars)}
enc = lambda s:[stoi[c] for c in s]
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

m = Poet(); m.load_state_dict(torch.load("poet.pth")); m.eval()

idx = torch.tensor([enc("【春天】")], dtype=torch.long)
with torch.no_grad():
    out = m(idx)            # 模型原始输出
print("输入：【春天】(4个字)")
print("模型输出形状：", tuple(out.shape), " = (1条, 4个位置, 每位置3569个字的分数)\n")

print("每个位置在预测“它后面的下一个字”，看各位置打分最高的5个字：\n")
labels = ["看到【之后", "看到【春之后", "看到【春天之后", "看到【春天】之后(★真正用这行)"]
for pos in range(4):
    row = out[0, pos]                      # 这个位置的3569个分数
    top = torch.topk(row, 5)               # 分数最高的5个
    pairs = [f"{itos[i.item()]}({row[i].item():.1f})" for i in top.indices]
    print(f"  位置{pos} {labels[pos]:18s}→ 最可能: {'  '.join(pairs)}")
