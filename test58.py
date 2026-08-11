# #单例模式
# import threading


# class Singleton:
#     _instance = None
#     _lock = threading.Lock()

#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             with cls._lock:
#                 # 获得锁后再次检查
#                 if cls._instance is None:
#                     cls._instance = super().__new__(cls)

#         return cls._instance


# singleton1 = Singleton()
# singleton2 = Singleton()

# print(singleton1 is singleton2)  # True


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    def __init__(self):
        print("只初始化一次")


a = Config()
b = Config()
print(type(a))
print(a is b)  # True