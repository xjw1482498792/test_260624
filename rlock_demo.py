"""演示 threading.RLock 相对 threading.Lock 的关键使用场景。

运行：python rlock_demo.py

场景：transfer_to() 已持有账户锁，随后调用同一个对象的 withdraw()；
withdraw() 作为可独立调用的线程安全公开方法，也必须获取同一把锁。
"""

from __future__ import annotations

import threading
from typing import Callable


class Account:
    def __init__(self, name: str, balance: int, lock_factory: Callable[[], object]):
        self.name = name
        self.balance = balance
        self._lock = lock_factory()

    def withdraw(self, amount: int) -> None:
        """既能单独调用，也能被其他持锁的公开方法调用。"""
        print(f"    withdraw(): 尝试再次获取 {self._lock!r}", flush=True)
        with self._lock:
            print("    withdraw(): 再次获取锁成功", flush=True)
            if amount > self.balance:
                raise ValueError("余额不足")
            self.balance -= amount

    def transfer_to(self, target: "Account", amount: int) -> None:
        """为突出重入问题，本例只讨论付款方账户锁。"""
        print("  transfer_to(): 第一次获取锁", flush=True)
        with self._lock:
            print("  transfer_to(): 已持有锁，调用也会加锁的 withdraw()", flush=True)
            self.withdraw(amount)
            target.balance += amount
            print("  transfer_to(): 转账完成", flush=True)


def run_case(lock_name: str, lock_factory: Callable[[], object]) -> None:
    print(f"\n{'=' * 18} 使用 {lock_name} {'=' * 18}")
    alice = Account("Alice", 100, lock_factory)
    bob = Account("Bob", 0, lock_factory)
    finished = threading.Event()

    def worker() -> None:
        alice.transfer_to(bob, 30)
        finished.set()

    # daemon=True：Lock 案例死锁后，不阻止演示进程退出。
    thread = threading.Thread(target=worker, daemon=True, name=f"{lock_name}-worker")
    thread.start()

    if not finished.wait(timeout=1.0):
        print("  结果：超时——同一线程第二次获取 Lock，发生自死锁。")
        print(f"  余额未完成更新：Alice={alice.balance}, Bob={bob.balance}")
        return

    thread.join()
    print(f"  结果：成功——Alice={alice.balance}, Bob={bob.balance}")


if __name__ == "__main__":
    run_case("Lock", threading.Lock)
    run_case("RLock", threading.RLock)

    print("\n结论：当一条调用链会让同一线程重复获取同一把锁时，必须使用 RLock，")
    print("或重新设计代码，拆出一个明确要求调用方已持锁的私有方法。")
