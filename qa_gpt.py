import os
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.stdout.reconfigure(encoding="utf-8")

# ── 教材：换成“问→答”样本，模型就能学会问答 ──────────
# 格式统一为：问：xxx？答：xxx。
qa_pairs = [
    ("你好",       "你好呀"),
    ("你叫什么",   "我叫小诗"),
    ("一加一等于几", "等于二"),
    ("天空什么颜色", "蓝色的"),
    ("你会做什么",   "我会背古诗"),
]
corpus = "".join(f"问：{q}？答：{a}。" for q, a in qa_pairs)

# ── 超参数（小，CPU 上几秒）──────────────────────────
BLOCK_SIZE = 48
EMBED_DIM  = 48
N_HEADS    = 4
N_LAYERS   = 3
LR         = 3e-3
STEPS      = 1500
BATCH_SIZE = 32
device     = "cpu"

# ── 数据：每个字编成数字 ─────────────────────────────
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

# ── 模型（和前两个同款 Transformer）──────────────────
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

class QAGPT(nn.Module):
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
    def ask(self, question):
        # 把问题套进“问：xxx？答：”的格式，让模型接着往下写答案
        prompt = f"问：{question}？答："
        # 万一问题里有教材没见过的字，先过滤（否则会报 KeyError）
        if any(c not in stoi for c in prompt):
            return "（问题里有我没学过的字，答不了）"
        idx = torch.tensor([encode(prompt)], dtype=torch.long)
        for _ in range(20):
            logits, _ = self(idx[:, -BLOCK_SIZE:])
            next_tok = logits[:, -1, :].argmax(dim=-1, keepdim=True)
            idx = torch.cat([idx, next_tok], dim=1)
            if itos[next_tok.item()] == "。":   # 答完一句就停
                break
        full = decode(idx[0].tolist())
        return full.split("答：")[1]   # 只返回“答：”后面那部分

# ── 训练 or 读档 ─────────────────────────────────────
CKPT = "qa.pth"
model = QAGPT()
print(f"模型参数量：{sum(p.numel() for p in model.parameters()):,}")
print(f"教材（{len(qa_pairs)} 条问答）：{corpus}\n")

if os.path.exists(CKPT):
    model.load_state_dict(torch.load(CKPT))
    model.eval()
    print(f"📂 发现存档 {CKPT}，直接读取，跳过训练！\n")
else:
    print("🆕 没有存档，开始从零训练……")
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
    print(f"💾 训练完成，已存档到 {CKPT}\n")

# ── 真正的问答测试 ───────────────────────────────────
print("========== 学过的问题（应该答得对）==========")
for q, _ in qa_pairs:
    print(f"我问：{q}？      它答：{model.ask(q)}")

print("\n========== 没学过的问题（会露馅）==========")
for q in ["二加二等于几", "你几岁"]:
    print(f"我问：{q}？      它答：{model.ask(q)}")

# ── 交互式提问：自己打字问它 ─────────────────────────
print("\n========== 轮到你了！输入问题回车提问，输入 q 退出 ==========")
print("（它只学过这几个问题：你好 / 你叫什么 / 一加一等于几 / 天空什么颜色 / 你会做什么）")
while True:
    q = input("\n你问：").strip()
    if q in ("q", "quit", "exit", ""):
        print("再见！")
        break
    print(f"它答：{model.ask(q)}")
