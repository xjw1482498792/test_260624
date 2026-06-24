import os, sys, torch
import torch.nn as nn
import torch.nn.functional as F
sys.stdout.reconfigure(encoding="utf-8")

# —— 和 tang_gpt.py 完全相同的教材与模型，这样才能加载 tang.pth ——
poems = {
    "静夜思":"床前明月光，疑是地上霜。举头望明月，低头思故乡。",
    "春晓":"春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。",
    "登鹳雀楼":"白日依山尽，黄河入海流。欲穷千里目，更上一层楼。",
    "相思":"红豆生南国，春来发几枝。愿君多采撷，此物最相思。",
    "鹿柴":"空山不见人，但闻人语响。返景入深林，复照青苔上。",
    "杂诗":"君自故乡来，应知故乡事。来日绮窗前，寒梅著花未。",
    "山中送别":"山中相送罢，日暮掩柴扉。春草明年绿，王孙归不归。",
    "江雪":"千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。",
    "寻隐者不遇":"松下问童子，言师采药去。只在此山中，云深不知处。",
    "登乐游原":"向晚意不适，驱车登古原。夕阳无限好，只是近黄昏。",
    "悯农":"锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。",
    "草":"离离原上草，一岁一枯荣。野火烧不尽，春风吹又生。",
    "八阵图":"功盖三分国，名成八阵图。江流石不转，遗恨失吞吴。",
    "鸟鸣涧":"人闲桂花落，夜静春山空。月出惊山鸟，时鸣春涧中。",
    "竹里馆":"独坐幽篁里，弹琴复长啸。深林人不知，明月来相照。",
    "终南望余雪":"终南阴岭秀，积雪浮云端。林表明霁色，城中增暮寒。",
    "渡汉江":"岭外音书断，经冬复历春。近乡情更怯，不敢问来人。",
    "问刘十九":"绿蚁新醅酒，红泥小火炉。晚来天欲雪，能饮一杯无。",
    "玉阶怨":"玉阶生白露，夜久侵罗袜。却下水晶帘，玲珑望秋月。",
    "怨情":"美人卷珠帘，深坐颦蛾眉。但见泪痕湿，不知心恨谁。",
}
SEP = "\n"
corpus = "".join(f"《{t}》{b}{SEP}" for t, b in poems.items())
BLOCK_SIZE, EMBED_DIM, N_HEADS, N_LAYERS = 64, 128, 4, 4
chars = sorted(set(corpus)); VOCAB_SIZE = len(chars)
stoi = {c:i for i,c in enumerate(chars)}; itos = {i:c for i,c in enumerate(chars)}
encode = lambda s:[stoi[c] for c in s]; decode = lambda l:"".join(itos[i] for i in l)
device = "cpu"

class Head(nn.Module):
    def __init__(s,hs):
        super().__init__()
        s.q=nn.Linear(EMBED_DIM,hs,bias=False); s.k=nn.Linear(EMBED_DIM,hs,bias=False); s.v=nn.Linear(EMBED_DIM,hs,bias=False)
        s.register_buffer("mask",torch.tril(torch.ones(BLOCK_SIZE,BLOCK_SIZE)))
    def forward(s,x):
        B,T,C=x.shape; q,k,v=s.q(x),s.k(x),s.v(x)
        a=q@k.transpose(-2,-1)*k.shape[-1]**-0.5
        a=a.masked_fill(s.mask[:T,:T]==0,float("-inf")); a=F.softmax(a,dim=-1)
        return a@v
class MultiHead(nn.Module):
    def __init__(s,nh,hs):
        super().__init__(); s.heads=nn.ModuleList([Head(hs) for _ in range(nh)]); s.proj=nn.Linear(EMBED_DIM,EMBED_DIM)
    def forward(s,x): return s.proj(torch.cat([h(x) for h in s.heads],dim=-1))
class FFN(nn.Module):
    def __init__(s):
        super().__init__(); s.net=nn.Sequential(nn.Linear(EMBED_DIM,4*EMBED_DIM),nn.ReLU(),nn.Linear(4*EMBED_DIM,EMBED_DIM))
    def forward(s,x): return s.net(x)
class Block(nn.Module):
    def __init__(s):
        super().__init__(); hs=EMBED_DIM//N_HEADS
        s.attn=MultiHead(N_HEADS,hs); s.ffn=FFN(); s.ln1=nn.LayerNorm(EMBED_DIM); s.ln2=nn.LayerNorm(EMBED_DIM)
    def forward(s,x):
        x=x+s.attn(s.ln1(x)); x=x+s.ffn(s.ln2(x)); return x
class TangGPT(nn.Module):
    def __init__(s):
        super().__init__()
        s.tok_emb=nn.Embedding(VOCAB_SIZE,EMBED_DIM); s.pos_emb=nn.Embedding(BLOCK_SIZE,EMBED_DIM)
        s.blocks=nn.Sequential(*[Block() for _ in range(N_LAYERS)]); s.ln_f=nn.LayerNorm(EMBED_DIM); s.head=nn.Linear(EMBED_DIM,VOCAB_SIZE)
    def forward(s,idx):
        B,T=idx.shape
        x=s.tok_emb(idx)+s.pos_emb(torch.arange(T,device=device)); x=s.ln_f(s.blocks(x))
        return s.head(x)

    @torch.no_grad()
    def compose(s, temperature=0.9):
        # 从“《”开始，按概率随机采样，自己编一首新诗
        idx = torch.tensor([encode("《")], dtype=torch.long)
        for _ in range(40):
            logits = s(idx[:, -BLOCK_SIZE:])[:, -1, :] / temperature
            probs = F.softmax(logits, dim=-1)
            nxt = torch.multinomial(probs, num_samples=1)   # 掷骰子选字，而不是选最确定的
            if itos[nxt.item()] == SEP:
                break
            idx = torch.cat([idx, nxt], dim=1)
        return decode(idx[0].tolist())

model = TangGPT()
model.load_state_dict(torch.load("tang.pth")); model.eval()
print("让模型自由作诗（每次随机，结果都不同）：\n")
for i in range(5):
    print(f"第{i+1}首：{model.compose(temperature=0.9)}")
