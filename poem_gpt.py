import os
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F

# Windows 控制台/重定向默认 GBK，会让中文输出变乱码，这里统一改成 UTF-8
sys.stdout.reconfigure(encoding="utf-8")

# ── 教材：一首古诗（李白《静夜思》）──────────────────
# 模型唯一的“课本”就是下面这 24 个字，它会被训练到把这首诗背下来
poem = "床前明月光，疑是地上霜。举头望明月，低头思故乡。"

# ── 超参数（都调小，CPU 上几秒跑完）────────────────
BLOCK_SIZE = len(poem) - 1   # 上下文长度：几乎覆盖全诗（留一位给“下一个字”做预测目标）
EMBED_DIM  = 32
N_HEADS    = 4
N_LAYERS   = 2
DROPOUT    = 0.0         # 背诵任务不需要防过拟合，我们就是要它“死记硬背”
LR         = 3e-3
STEPS      = 800
BATCH_SIZE = 16

device = "cpu"

# ── 数据准备：把每个汉字编成数字 ─────────────────────
chars = sorted(set(poem))
VOCAB_SIZE = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for i, c in enumerate(chars)}
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: "".join(itos[i] for i in l)

data = torch.tensor(encode(poem), dtype=torch.long)

def get_batch():
    # 从全诗里随机截取一些 (输入, 下一个字) 的小窗口来训练
    ix = torch.randint(len(data) - BLOCK_SIZE, (BATCH_SIZE,)) if len(data) > BLOCK_SIZE \
         else torch.zeros(BATCH_SIZE, dtype=torch.long)
    x = torch.stack([data[i:i+BLOCK_SIZE]     for i in ix])
    y = torch.stack([data[i+1:i+BLOCK_SIZE+1] for i in ix])
    return x, y

# ── 模型（和 mini_gpt.py 同款 Transformer，只是更小）──

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
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        return self.proj(out)

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

class PoemGPT(nn.Module):
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
    def recite(self, start_char):
        # 给一个起始字，让它一个字一个字往下背，直到补满整首诗的长度
        idx = torch.tensor([[stoi[start_char]]], dtype=torch.long)
        for _ in range(len(poem) - 1):
            logits, _ = self(idx[:, -BLOCK_SIZE:])
            next_tok = logits[:, -1, :].argmax(dim=-1, keepdim=True)  # 取最有把握的那个字
            idx = torch.cat([idx, next_tok], dim=1)
        return decode(idx[0].tolist())

# ── 训练 or 读档 ─────────────────────────────────────
CKPT = "poem.pth"   # 存档文件：训练好的参数会存在这里

model = PoemGPT()
print(f"模型参数量：{sum(p.numel() for p in model.parameters()):,}")
print(f"课本（全诗）：{poem}\n")

if os.path.exists(CKPT):
    # ── 读档：已有训练好的参数，直接加载，跳过训练 ──
    model.load_state_dict(torch.load(CKPT))
    model.eval()
    print(f"📂 发现存档 {CKPT}，直接读取，跳过训练！")
else:
    # ── 第一次：从零训练，然后存档 ──
    print("🆕 没有存档，开始从零训练……")
    print(f"训练前，让它从“床”开始背 → {model.recite('床')}\n")
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)
    for step in range(STEPS):
        xb, yb = get_batch()
        _, loss = model(xb, yb)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if step % 100 == 0 or step == STEPS - 1:
            print(f"step {step:4d} | loss: {loss.item():.4f}")
    torch.save(model.state_dict(), CKPT)
    print(f"\n💾 训练完成，已存档到 {CKPT}（下次再跑就不用重训了）")

# ── 检验：它背下来了吗？─────────────────────────────
print(f"\n让它从“床”开始背 → {model.recite('床')}")
print(f"对照原诗　　　　 → {poem}")
print(f"背对了吗？{'✅ 一字不差！' if model.recite('床') == poem else '❌ 还有错'}")
