import threading


class LogHandler:
    def __init__(self, name, registry):
        self.name = name
        self.registry = registry

    def register(self):
        self.registry.register_handler(self)


class LoggingRegistry:
    def __init__(self, lock):
        self.lock = lock
        self.handlers = {}

    def configure_handler(self, name):
        thread_name = threading.current_thread().name
        print(f"{thread_name}：第一次获取注册中心锁，开始配置 Handler")

        with self.lock:
            handler = LogHandler(name, self)
            print(f"{thread_name}：Handler 配置完成，回调注册中心")
            handler.register()
            print(f"{thread_name}：配置流程完成")

    def register_handler(self, handler):
        thread_name = threading.current_thread().name
        print(f"{thread_name}：第二次获取同一把注册中心锁，注册 Handler")

        with self.lock:
            self.handlers[handler.name] = handler
            print(f"{thread_name}：注册成功")


def run_demo(lock_factory, title, daemon):
    print(f"\n========== {title} ==========")
    registry = LoggingRegistry(lock_factory())
    thread = threading.Thread(
        target=registry.configure_handler,
        args=("console",),
        name=f"{title}配置线程",
        daemon=daemon,
    )

    thread.start()

    if daemon:
        thread.join(timeout=1)
    else:
        thread.join()

    if thread.is_alive():
        print(f"{title}：1 秒内没有完成，卡在第二次获取同一把锁。")
    else:
        print(f"{title}：完成，已注册 {list(registry.handlers)}")


def main():
    run_demo(threading.Lock, "普通 Lock", daemon=True)
    run_demo(threading.RLock, "RLock", daemon=False)


if __name__ == "__main__":
    main()
