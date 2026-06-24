import os
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.stdout.reconfigure(encoding="utf-8")

# ── 教材：20 首唐诗名篇，格式「《诗名》全诗」───────────
poems = {
    "静夜思":   "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
    "春晓":     "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。",
    "登鹳雀楼": "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。",
    "相思":     "红豆生南国，春来发几枝。愿君多采撷，此物最相思。",
    "鹿柴":     "空山不见人，但闻人语响。返景入深林，复照青苔上。",
    "杂诗":     "君自故乡来，应知故乡事。来日绮窗前，寒梅著花未。",
    "山中送别": "山中相送罢，日暮掩柴扉。春草明年绿，王孙归不归。",
    "江雪":     "千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。",
    "寻隐者不遇":"松下问童子，言师采药去。只在此山中，云深不知处。",
    "登乐游原": "向晚意不适，驱车登古原。夕阳无限好，只是近黄昏。",
    "悯农":     "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。",
    "草":       "离离原上草，一岁一枯荣。野火烧不尽，春风吹又生。",
    "八阵图":   "功盖三分国，名成八阵图。江流石不转，遗恨失吞吴。",
    "鸟鸣涧":   "人闲桂花落，夜静春山空。月出惊山鸟，时鸣春涧中。",
    "竹里馆":   "独坐幽篁里，弹琴复长啸。深林人不知，明月来相照。",
    "终南望余雪":"终南阴岭秀，积雪浮云端。林表明霁色，城中增暮寒。",
    "渡汉江":   "岭外音书断，经冬复历春。近乡情更怯，不敢问来人。",
    "问刘十九": "绿蚁新醅酒，红泥小火炉。晚来天欲雪，能饮一杯无。",
    "玉阶怨":   "玉阶生白露，夜久侵罗袜。却下水晶帘，玲珑望秋月。",
    "怨情":     "美人卷珠帘，深坐颦蛾眉。但见泪痕湿，不知心恨谁。",
}
SEP = "\n"  # 每首诗结尾的分隔符，也是“背完一首”的停止信号
corpus = "".join(f"《{t}》{b}{SEP}" for t, b in poems.items())

# ── 超参数（比背一首大很多，因为教材多了 20 倍）──────
BLOCK_SIZE = 64
EMBED_DIM  = 128
N_HEADS    = 4
N_LAYERS   = 4
LR         = 3e-3
STEPS      = 3000
BATCH_SIZE = 64
device     = "cpu"

# ── 数据 ─────────────────────────────────────────────
chars = sorted(set(corpus))
VOCAB_SIZE = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for i, c in enumerate(chars)}
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: "".join(itos[i] for i in l)
data = torch.tensor(encode(corpus), dtype=torch.long)

def get_batch():
    ix = torch.randint(len(data) - BLOCK_SIZE, (BATCH_SIZE,))
    x = torch.stack([data[i:i+BLOCK_SIZE]     for i in ix])
    y = torch.stack([data[i+1:i+BLOCK_SIZE+1] for i in ix])
    return x, y

# ── 模型（同款 Transformer）──────────────────────────
class Head(nn.Module):
    def __init__(self, head_size):
        super().__init__()
        self.q = nn.Linear(EMBED_DIM, head_size, bias=False)
        self.k = nn.Linear(EMBED_DIM, head_size, bias=False)
        self.v = nn.Linear(EMBED_DIM, head_size, bias=False)
        self.register_buffer("mask", torch.tril(torch.ones(BLOCK_SIZE, BLOCK_SIZE)))
    def forward(self, x):
        B, T, C = x.shape
        q, k, v = self.q(x), self.k(x), self.v(x)
        attn = q @ k.transpose(-2, -1) * k.shape[-1] ** -0.5
        attn = attn.masked_fill(self.mask[:T, :T] == 0, float("-inf"))
        attn = F.softmax(attn, dim=-1)
        return attn @ v

class MultiHead(nn.Module):
    def __init__(self, n_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(n_heads)])
        self.proj  = nn.Linear(EMBED_DIM, EMBED_DIM)
    def forward(self, x):
        return self.proj(torch.cat([h(x) for h in self.heads], dim=-1))

class FFN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(EMBED_DIM, 4 * EMBED_DIM), nn.ReLU(),
            nn.Linear(4 * EMBED_DIM, EMBED_DIM),
        )
    def forward(self, x):
        return self.net(x)

class Block(nn.Module):
    def __init__(self):
        super().__init__()
        head_size = EMBED_DIM // N_HEADS
        self.attn = MultiHead(N_HEADS, head_size)
        self.ffn  = FFN()
        self.ln1  = nn.LayerNorm(EMBED_DIM)
        self.ln2  = nn.LayerNorm(EMBED_DIM)
    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.ffn(self.ln2(x))
        return x

class TangGPT(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok_emb = nn.Embedding(VOCAB_SIZE, EMBED_DIM)
        self.pos_emb = nn.Embedding(BLOCK_SIZE, EMBED_DIM)
        self.blocks  = nn.Sequential(*[Block() for _ in range(N_LAYERS)])
        self.ln_f    = nn.LayerNorm(EMBED_DIM)
        self.head    = nn.Linear(EMBED_DIM, VOCAB_SIZE)
    def forward(self, idx, targets=None):
        B, T = idx.shape
        x = self.tok_emb(idx) + self.pos_emb(torch.arange(T, device=device))
        x = self.ln_f(self.blocks(x))
        logits = self.head(x)
        loss = None
        if targets is not None:
            B, T, V = logits.shape
            loss = F.cross_entropy(logits.view(B*T, V), targets.view(B*T))
        return logits, loss

    @torch.no_grad()
    def recite(self, title):
        prompt = f"《{title}》"
        if any(c not in stoi for c in prompt):
            return "（诗名里有我没学过的字，背不了）"
        idx = torch.tensor([encode(prompt)], dtype=torch.long)
        for _ in range(40):
            logits, _ = self(idx[:, -BLOCK_SIZE:])
            next_tok = logits[:, -1, :].argmax(dim=-1, keepdim=True)
            if itos[next_tok.item()] == SEP:   # 背完一首就停
                break
            idx = torch.cat([idx, next_tok], dim=1)
        return decode(idx[0].tolist()).split("》", 1)[1]

# ── 训练 or 读档 ─────────────────────────────────────
CKPT = "tang.pth"
model = TangGPT()
print(f"模型参数量：{sum(p.numel() for p in model.parameters()):,}")
print(f"教材：20 首唐诗，共认识 {VOCAB_SIZE} 个字\n")

if os.path.exists(CKPT):
    model.load_state_dict(torch.load(CKPT))
    model.eval()
    print(f"📂 发现存档 {CKPT}，直接读取，跳过训练！")
else:
    print("🆕 没有存档，开始从零训练……（CPU 上约一两分钟）")
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)
    for step in range(STEPS):
        xb, yb = get_batch()
        _, loss = model(xb, yb)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if step % 300 == 0 or step == STEPS - 1:
            print(f"step {step:4d} | loss: {loss.item():.4f}")
    torch.save(model.state_dict(), CKPT)
    print(f"💾 训练完成，已存档到 {CKPT}")

# ── 抽查：随便背几首看准不准 ─────────────────────────
print("\n========== 抽查（对照原诗）==========")
ok = 0
for t, b in poems.items():
    got = model.recite(t)
    good = got == b
    ok += good
    print(f"{'✅' if good else '❌'}《{t}》{got}")
print(f"\n20 首里背对了 {ok} 首")

# ── 交互：自己输入诗名让它背 ─────────────────────────
print("\n========== 输入诗名让它背，输入 q 退出 ==========")
print("可背：" + "、".join(poems.keys()))
while True:
    t = input("\n诗名：").strip().strip("《》")
    if t in ("q", "quit", "exit", ""):
        print("再见！")
        break
    print(f"《{t}》{model.recite(t)}")
