import sys, torch
import torch.nn as nn
import torch.nn.functional as F
sys.stdout.reconfigure(encoding="utf-8")

poems = {
    "静夜思":"床前明月光，疑是地上霜。举头望明月，低头思故乡。","春晓":"春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。",
    "登鹳雀楼":"白日依山尽，黄河入海流。欲穷千里目，更上一层楼。","相思":"红豆生南国，春来发几枝。愿君多采撷，此物最相思。",
    "鹿柴":"空山不见人，但闻人语响。返景入深林，复照青苔上。","杂诗":"君自故乡来，应知故乡事。来日绮窗前，寒梅著花未。",
    "山中送别":"山中相送罢，日暮掩柴扉。春草明年绿，王孙归不归。","江雪":"千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。",
    "寻隐者不遇":"松下问童子，言师采药去。只在此山中，云深不知处。","登乐游原":"向晚意不适，驱车登古原。夕阳无限好，只是近黄昏。",
    "悯农":"锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。","草":"离离原上草，一岁一枯荣。野火烧不尽，春风吹又生。",
    "八阵图":"功盖三分国，名成八阵图。江流石不转，遗恨失吞吴。","鸟鸣涧":"人闲桂花落，夜静春山空。月出惊山鸟，时鸣春涧中。",
    "竹里馆":"独坐幽篁里，弹琴复长啸。深林人不知，明月来相照。","终南望余雪":"终南阴岭秀，积雪浮云端。林表明霁色，城中增暮寒。",
    "渡汉江":"岭外音书断，经冬复历春。近乡情更怯，不敢问来人。","问刘十九":"绿蚁新醅酒，红泥小火炉。晚来天欲雪，能饮一杯无。",
    "玉阶怨":"玉阶生白露，夜久侵罗袜。却下水晶帘，玲珑望秋月。","怨情":"美人卷珠帘，深坐颦蛾眉。但见泪痕湿，不知心恨谁。",
}
SEP="\n"; corpus="".join(f"《{t}》{b}{SEP}" for t,b in poems.items())
# 把所有原诗的“句子”收集起来，用于查重
orig_lines = set()
for b in poems.values():
    for line in b.replace("。","，").split("，"):
        if line: orig_lines.add(line)

BLOCK_SIZE, EMBED_DIM, N_HEADS, N_LAYERS = 64, 24, 4, 2   # 中等偏小：能学结构，难背全
STEPS, LR, BATCH = 2500, 3e-3, 64
chars=sorted(set(corpus)); V=len(chars)
stoi={c:i for i,c in enumerate(chars)}; itos={i:c for i,c in enumerate(chars)}
enc=lambda s:[stoi[c] for c in s]; dec=lambda l:"".join(itos[i] for i in l)
data=torch.tensor(enc(corpus),dtype=torch.long)
def batch():
    ix=torch.randint(len(data)-BLOCK_SIZE,(BATCH,))
    return torch.stack([data[i:i+BLOCK_SIZE] for i in ix]),torch.stack([data[i+1:i+BLOCK_SIZE+1] for i in ix])

class Head(nn.Module):
    def __init__(s,h):
        super().__init__(); s.q=nn.Linear(EMBED_DIM,h,bias=False); s.k=nn.Linear(EMBED_DIM,h,bias=False); s.v=nn.Linear(EMBED_DIM,h,bias=False)
        s.register_buffer("m",torch.tril(torch.ones(BLOCK_SIZE,BLOCK_SIZE)))
    def forward(s,x):
        B,T,C=x.shape; a=s.q(x)@s.k(x).transpose(-2,-1)*s.k(x).shape[-1]**-0.5
        a=F.softmax(a.masked_fill(s.m[:T,:T]==0,float("-inf")),dim=-1); return a@s.v(x)
class MH(nn.Module):
    def __init__(s,n,h):
        super().__init__(); s.h=nn.ModuleList([Head(h) for _ in range(n)]); s.p=nn.Linear(EMBED_DIM,EMBED_DIM)
    def forward(s,x): return s.p(torch.cat([h(x) for h in s.h],dim=-1))
class FFN(nn.Module):
    def __init__(s): super().__init__(); s.n=nn.Sequential(nn.Linear(EMBED_DIM,4*EMBED_DIM),nn.ReLU(),nn.Linear(4*EMBED_DIM,EMBED_DIM))
    def forward(s,x): return s.n(x)
class Blk(nn.Module):
    def __init__(s):
        super().__init__(); s.a=MH(N_HEADS,EMBED_DIM//N_HEADS); s.f=FFN(); s.l1=nn.LayerNorm(EMBED_DIM); s.l2=nn.LayerNorm(EMBED_DIM)
    def forward(s,x): x=x+s.a(s.l1(x)); return x+s.f(s.l2(x))
class M(nn.Module):
    def __init__(s):
        super().__init__(); s.te=nn.Embedding(V,EMBED_DIM); s.pe=nn.Embedding(BLOCK_SIZE,EMBED_DIM)
        s.b=nn.Sequential(*[Blk() for _ in range(N_LAYERS)]); s.lf=nn.LayerNorm(EMBED_DIM); s.hd=nn.Linear(EMBED_DIM,V)
    def forward(s,idx,tg=None):
        B,T=idx.shape; x=s.te(idx)+s.pe(torch.arange(T)); x=s.lf(s.b(x)); lg=s.hd(x)
        if tg is None: return lg,None
        B,T,Vv=lg.shape; return lg,F.cross_entropy(lg.view(B*T,Vv),tg.view(B*T))
    @torch.no_grad()
    def compose(s,temp=1.0):
        idx=torch.tensor([enc("《")],dtype=torch.long)
        for _ in range(40):
            lg=s(idx[:,-BLOCK_SIZE:])[0][:,-1,:]/temp
            nx=torch.multinomial(F.softmax(lg,dim=-1),1)
            if itos[nx.item()]==SEP: break
            idx=torch.cat([idx,nx],dim=1)
        return dec(idx[0].tolist())

m=M()
print(f"模型参数量：{sum(p.numel() for p in m.parameters()):,}\n")
opt=torch.optim.AdamW(m.parameters(),lr=LR)
for step in range(STEPS):
    xb,yb=batch(); _,loss=m(xb,yb); opt.zero_grad(); loss.backward(); opt.step()
print("生成 8 首，逐句检查是【抄的】还是【新造的】：\n")
for i in range(8):
    poem=m.compose(temp=1.0)
    body=poem.split("》",1)[1] if "》" in poem else poem
    lines=[ln for ln in body.replace("。","，").split("，") if ln]
    tags=["抄" if ln in orig_lines else "新" for ln in lines]
    newcount=tags.count("新")
    print(f"第{i+1}首：{poem}")
    print(f"      句子标记：{tags}  →  其中 {newcount}/{len(tags)} 句是原诗里没有的新句\n")
