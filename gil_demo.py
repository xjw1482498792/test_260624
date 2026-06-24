import sys, time, threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
sys.stdout.reconfigure(encoding="utf-8")

def cpu_task(n=50_000_000):
    """纯计算任务，让CPU一直忙"""
    total = 0
    for i in range(n):
        total += i
    return total

if __name__ == '__main__':
    print("=" * 55)
    print("GIL 演示：CPU密集型任务，多线程并不能真正并行")
    print("=" * 55)

    # ── 单线程跑2次 ──────────────────────────────────────
    t0 = time.time()
    cpu_task()
    cpu_task()
    single = time.time() - t0
    print(f"\n单线程跑2次:  {single:.2f} 秒")

    # ── 多线程跑2次（受GIL限制，不能真正并行）──────────────
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=2) as pool:
        f1 = pool.submit(cpu_task)
        f2 = pool.submit(cpu_task)
        f1.result(); f2.result()
    thread = time.time() - t0
    print(f"多线程跑2次:  {thread:.2f} 秒  ← 和单线程差不多！GIL让它们轮流跑")

    # ── 多进程跑2次（绕过GIL，真正并行）───────────────────
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=2) as pool:
        f1 = pool.submit(cpu_task)
        f2 = pool.submit(cpu_task)
        f1.result(); f2.result()
    process = time.time() - t0
    print(f"多进程跑2次:  {process:.2f} 秒  ← 真正并行，速度接近单线程的一半！")

    print(f"\n加速比对比:")
    print(f"  多线程 vs 单线程: {single/thread:.2f}x  （接近1，说明没有加速）")
    print(f"  多进程 vs 单线程: {single/process:.2f}x  （接近2，说明真正并行）")

    print("\n" + "=" * 55)
    print("结论：GIL导致多线程无法加速CPU密集型任务")
    print("      CPU密集 → 用多进程 | IO密集 → 用多线程")
    print("=" * 55)
