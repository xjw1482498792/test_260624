# import threading

# lock = threading.Lock()

# with lock:
#     # 操作共享数据
#     pass



# lock = threading.RLock()

# with lock:
#     with lock:
#         pass

# semaphore = threading.Semaphore(3)

# with semaphore:
#     # 使用有限资源
#     pass    

# import threading

# lock = threading.RLock()

# def inner():
#     with lock:
#         print("inner")

# def outer():
#     with lock:
#         inner()  # 同一线程再次获取同一把锁

import threading


class LockDemo:
    """普通 Lock 演示"""

    def __init__(self):
        self.lock = threading.Lock()
        self.balance = 100

    def add_money(self, amount):
        print("    add_money：尝试再次获取 Lock")

        # 如果不设置 timeout，这里会永久等待，形成自我死锁
        acquired = self.lock.acquire(timeout=2)

        if not acquired:
            print("    add_money：获取失败，同一个线程不能重复获取 Lock")
            return

        try:
            self.balance += amount
        finally:
            self.lock.release()

    def update_balance(self):
        print("update_balance：第一次获取 Lock")

        with self.lock:
            print("update_balance：获取成功")
            self.add_money(50)
        # print("可以执行")

        print(f"Lock 最终余额：{self.balance}")


class RLockDemo:
    """可重入锁 RLock 演示"""

    def __init__(self):
        self.lock = threading.RLock()
        self.balance = 100

    def add_money(self, amount):
        print("    add_money：尝试再次获取 RLock")

        with self.lock:
            print("    add_money：重复获取成功")
            self.balance += amount
            print(f"    add_money：余额增加 {amount}")

    def update_balance(self):
        print("update_balance：第一次获取 RLock")

        with self.lock:
            print("update_balance：获取成功")
            self.add_money(50)
        

        print(f"RLock 最终余额：{self.balance}")


def run_lock_demo():
    print("========== 普通 Lock ==========")

    demo = LockDemo()
    thread = threading.Thread(
        target=demo.update_balance,
        name="Lock线程"
    )

    thread.start()
    thread.join()
    # pass


def run_rlock_demo():
    print("\n========== 可重入 RLock ==========")

    demo = RLockDemo()
    thread = threading.Thread(
        target=demo.update_balance,
        name="RLock线程"
    )

    thread.start()
    thread.join()


if __name__ == "__main__":
    run_lock_demo()
    run_rlock_demo()