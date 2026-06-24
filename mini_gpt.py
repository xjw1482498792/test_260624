import sys
import torch
import torch.nn as nn
import torch.nn.functional as F

# Windows 控制台/重定向默认 GBK，会让中文输出变乱码，这里统一改成 UTF-8
sys.stdout.reconfigure(encoding="utf-8")

# ── 超参数 ──────────────────────────────────────────
VOCAB_SIZE  = 65       # 字符集大小（a-z A-Z 标点等）
BLOCK_SIZE  = 64       # 最大上下文长度（一次看多少字符）
EMBED_DIM   = 64       # 每个 token 的向量维度
N_HEADS     = 4        # 多头注意力的头数
N_LAYERS    = 3        # Transformer Block 层数
DROPOUT     = 0.1
LR          = 3e-3
STEPS       = 3000
BATCH_SIZE  = 32

device = "cuda" if torch.cuda.is_available() else "cpu"

# ── 数据准备 ─────────────────────────────────────────
text = open(__file__, encoding="utf-8").read()  # 用代码自身当训练数据（能跑就行）

chars = sorted(set(text))
VOCAB_SIZE = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for i, c in enumerate(chars)}
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: "".join(itos[i] for i in l)

data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9 * len(data))
train_data, val_data = data[:n], data[n:]

def get_batch(split):
    d = train_data if split == "train" else val_data
    ix = torch.randint(len(d) - BLOCK_SIZE, (BATCH_SIZE,))
    x = torch.stack([d[i:i+BLOCK_SIZE] for i in ix])
    y = torch.stack([d[i+1:i+BLOCK_SIZE+1] for i in ix])
    return x.to(device), y.to(device)

# ── 模型组件 ─────────────────────────────────────────

class Head(nn.Module):
    """单头 Self-Attention"""
    def __init__(self, head_size):
        super().__init__()
        self.q = nn.Linear(EMBED_DIM, head_size, bias=False)
        self.k = nn.Linear(EMBED_DIM, head_size, bias=False)
        self.v = nn.Linear(EMBED_DIM, head_size, bias=False)
        # 因果掩码：只能看到自己左边的词
        self.register_buffer("mask", torch.tril(torch.ones(BLOCK_SIZE, BLOCK_SIZE)))
        self.drop = nn.Dropout(DROPOUT)

    def forward(self, x):
        B, T, C = x.shape
        q = self.q(x)                              # (B, T, head_size)
        k = self.k(x)
        v = self.v(x)
        # 注意力分数
        scale = k.shape[-1] ** -0.5
        attn = q @ k.transpose(-2, -1) * scale    # (B, T, T)
        attn = attn.masked_fill(self.mask[:T,:T] == 0, float("-inf"))
        attn = F.softmax(attn, dim=-1)
        attn = self.drop(attn)
        return attn @ v                            # (B, T, head_size)

class MultiHead(nn.Module):
    """多头注意力 = 并行跑多个 Head，拼在一起"""
    def __init__(self, n_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(n_heads)])
        self.proj  = nn.Linear(EMBED_DIM, EMBED_DIM)
        self.drop  = nn.Dropout(DROPOUT)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)  # 拼接各头输出
        return self.drop(self.proj(out))

class FFN(nn.Module):
    """Feed Forward Network：每个位置独立的两层 MLP"""
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(EMBED_DIM, 4 * EMBED_DIM),
            nn.ReLU(),
            nn.Linear(4 * EMBED_DIM, EMBED_DIM),
            nn.Dropout(DROPOUT),
        )

    def forward(self, x):
        return self.net(x)

class Block(nn.Module):
    """一个完整的 Transformer Block = 多头注意力 + FFN + 残差 + LayerNorm"""
    def __init__(self):
        super().__init__()
        head_size = EMBED_DIM // N_HEADS
        self.attn = MultiHead(N_HEADS, head_size)
        self.ffn  = FFN()
        self.ln1  = nn.LayerNorm(EMBED_DIM)
        self.ln2  = nn.LayerNorm(EMBED_DIM)

    def forward(self, x):
        x = x + self.attn(self.ln1(x))   # 残差连接
        x = x + self.ffn(self.ln2(x))
        return x

class MiniGPT(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok_emb = nn.Embedding(VOCAB_SIZE, EMBED_DIM)   # 词向量
        self.pos_emb = nn.Embedding(BLOCK_SIZE, EMBED_DIM)   # 位置编码
        self.blocks  = nn.Sequential(*[Block() for _ in range(N_LAYERS)])
        self.ln_f    = nn.LayerNorm(EMBED_DIM)
        self.head    = nn.Linear(EMBED_DIM, VOCAB_SIZE)      # 输出层：预测下一个字符

    def forward(self, idx, targets=None):
        B, T = idx.shape
        tok  = self.tok_emb(idx)                             # (B, T, C)
        pos  = self.pos_emb(torch.arange(T, device=device)) # (T, C)
        x    = tok + pos
        x    = self.blocks(x)
        x    = self.ln_f(x)
        logits = self.head(x)                                # (B, T, vocab)

        loss = None
        if targets is not None:
            B, T, V = logits.shape
            loss = F.cross_entropy(logits.view(B*T, V), targets.view(B*T))
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new=200):
        for _ in range(max_new):
            idx_cond = idx[:, -BLOCK_SIZE:]
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :]                        # 只取最后一个位置
            probs  = F.softmax(logits, dim=-1)
            next_tok = torch.multinomial(probs, num_samples=1)
            idx = torch.cat([idx, next_tok], dim=1)
        return idx

# ── 训练 ─────────────────────────────────────────────

model = MiniGPT().to(device)
total_params = sum(p.numel() for p in model.parameters())
print(f"模型参数量：{total_params:,}")
print(f"使用设备：{device}\n")

optimizer = torch.optim.AdamW(model.parameters(), lr=LR)

for step in range(STEPS):
    xb, yb = get_batch("train")
    logits, loss = model(xb, yb)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if step % 500 == 0 or step == STEPS - 1:
        model.eval()
        with torch.no_grad():
            _, val_loss = model(*get_batch("val"))
        print(f"step {step:4d} | train loss: {loss.item():.4f} | val loss: {val_loss.item():.4f}")
        model.train()

# ── 生成文本 ──────────────────────────────────────────
print("\n── 生成文本 ──")
model.eval()
start = torch.zeros((1, 1), dtype=torch.long, device=device)
output = decode(model.generate(start, max_new=300)[0].tolist())
print(output)
