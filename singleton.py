"""线程安全的单例模式实现。"""

from threading import Lock
from typing import Any


class SingletonMeta(type):
    """确保使用该元类的每个类在进程内只有一个实例。"""

    _instances: dict[type, Any] = {}
    _lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            with cls._lock:
                # 双重检查，避免多个线程同时创建实例。
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AppConfig(metaclass=SingletonMeta):
    """单例模式的使用示例。"""

    def __init__(self, environment: str = "development") -> None:
        self.environment = environment


if __name__ == "__main__":
    first = AppConfig("production")
    second = AppConfig("testing")

    print(first is second)  # True
    print(second.environment)  # production
