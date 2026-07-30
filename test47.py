def repeat(count):           # 装饰器参数
    def decorator(func):     # 接收原函数
        def wrapper(*args, **kwargs):  # 接收原函数参数
            for _ in range(count):
                result = func(*args, **kwargs)
            return result

        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"你好，{name}")

greet("小明")

def out_fun(count:int = 3):
    def dec_fun1(ori_fun):
        def warper(*args, **kwargs):
            print("before")
            for _ in range(count):
                print(ori_fun(*args, **kwargs))
            print("after")
        return warper    
    return dec_fun1

@out_fun()
def fun1(name)-> str:
    return name + "IS ME"



fun1("XIAOMING")



print("------------")
def fun3_dec(fun):
    def wrapper():
        print("BEFORE")
        fun()
        print("AFTER")
    return wrapper    
@fun3_dec        
def fun3():
    print("FUN3")

fun3()    


#迭代器
print("---------")
class Counter:
    def __init__(self, end):
        self.current = 1
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.end:
            raise StopIteration

        value = self.current
        self.current += 1
        return value


counter = Counter(3)

print(next(counter))  # 1
print(next(counter))  # 2
print(next(counter))  # 3

