import os, sys, time, torch
import torch.nn as nn
import torch.nn.functional as F
sys.stdout.reconfigure(encoding="utf-8")

text = open("poems_data.txt", encoding="utf-8").read()
chars = sorted(set(text)); V = len(chars)
stoi = {c:i for i,c in enumerate(chars)}; itos = {i:c for i,c in enumerate(chars)}
enc = lambda s:[stoi[c] for c in s]; dec = lambda l:"".join(itos[i] for i in l)
data = torch.tensor(enc(text), dtype=torch.long)

# ── 模型配置（适中：装得下规律，装不下 3700 首原文）──
BLOCK_SIZE, EMBED_DIM, N_HEADS, N_LAYERS, DROPOUT = 48, 192, 6, 5, 0.1
LR, BATCH, STEPS, CKPT_EVERY = 3e-3, 64, 8000, 500
CKPT = "poet.pth"

def get_batch():
    ix = torch.randint(len(data)-BLOCK_SIZE, (BATCH,))
    return (torch.stack([data[i:i+BLOCK_SIZE] for i in ix]),
            torch.stack([data[i+1:i+BLOCK_SIZE+1] for i in ix]))

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
    def forward(s,idx,tg=None):
        B,T=idx.shape; x=s.te(idx)+s.pe(torch.arange(T)); x=s.lf(s.b(x)); lg=s.hd(x)
        if tg is None: return lg,None
        B,T,Vv=lg.shape; return lg,F.cross_entropy(lg.view(B*T,Vv),tg.view(B*T))
    @torch.no_grad()
    def write(s, theme, temp=0.85, topk=20):
        s.eval()
        prompt = f"【{theme}】"
        idx = torch.tensor([enc(prompt)], dtype=torch.long)
        for _ in range(40):
            lg = s(idx[:,-BLOCK_SIZE:])[0][:,-1,:]/temp
            v,_ = torch.topk(lg, topk); lg[lg < v[:,[-1]]] = -float("inf")
            nx = torch.multinomial(F.softmax(lg,dim=-1),1)
            if itos[nx.item()] == "\n": break
            idx = torch.cat([idx,nx],dim=1)
        s.train()
        return dec(idx[0].tolist())

m = Poet()
print(f"模型参数量：{sum(p.numel() for p in m.parameters()):,}")
print(f"训练数据：{len(text):,} 字，认识 {V} 个字，共 3714 首绝句\n", flush=True)
opt = torch.optim.AdamW(m.parameters(), lr=LR)
t0 = time.time()
for step in range(STEPS):
    xb,yb = get_batch(); _,loss = m(xb,yb); opt.zero_grad(); loss.backward(); opt.step()
    if step % 200 == 0 or step == STEPS-1:
        print(f"step {step:5d} | loss {loss.item():.3f} | 用时 {time.time()-t0:.0f}s", flush=True)
    if step % 1000 == 0 and step > 0:
        print(f"   [春天] {m.write('春天')}", flush=True)
        print(f"   [爱情] {m.write('爱情')}", flush=True)
    if step % CKPT_EVERY == 0 and step > 0:
        torch.save(m.state_dict(), CKPT)
torch.save(m.state_dict(), CKPT)
print(f"\n训练完成，已存档 {CKPT}", flush=True)
