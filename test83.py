#手写定时装饰器
import time
def deco_fun(ori):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = ori(*args, **kwargs)
        end = time.time()
        print(f'总耗时：{end - start}秒')
        return res
    return wrapper
@deco_fun
def ori_fun():
    time.sleep(2)
    return ("origin function is running")


#生成器
def gen1(begin, end):
    while begin <= end:
        yield begin
        begin += 1

if __name__ == "__main__":
    # print(ori_fun())
    my_gen = gen1(0, 5)
    print(next(my_gen))
    print(next(my_gen))
