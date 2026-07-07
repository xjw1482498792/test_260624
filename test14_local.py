# #元组 列表 字典 集合 数字 布尔 字符
# print('元组 列表 字典 集合 数字 布尔 字符')
# tuple1 = (1, 1, 3)
# print(f'tuple1: {tuple1}')

# list1 = [1, 2, 3]
# print(f'list1: {list1}')

# dict1 = {(1, 2, 3): "value1", (4, 5, 6): "value2"}
# print(f'dict1: {dict1}')

# #元组不可变 列表可变
# # dect2 = {[1,2,3]: "value1", [4,5,6]: "value2"}
# print('#元组不可变 列表可变')
# list1[0] = 10
# print(f'list1 after modification: {list1}')
# # tuple1[0] = 10  # This will raise an error because tuples are immutable
# tuple1 = tuple1 + (4,)
# print(f'tuple1 after adding an element: {tuple1}')  

# #验证元组地址原理
# t = (10, 20)
# print(f'address of t: {id(t)}')
# print(f'address of t[0]: {id(t[0])}')
# print(f'address of t[1]: {id(t[1])}')

# #所以得出结论list不可以做字典的key，而tuple元组可以
# #tuple不变，hash稳定


#练习  手写装饰器

def fun1(func_tmp):
    def wrapper(*args, **kwargs):
        print('args:', args)
        print('kwargs:', kwargs)
        res = func_tmp(*args, **kwargs)
        print('finished')
        # return res
    return wrapper

@fun1
def func(arg0, arg1):
    return(arg0 + arg1)


func(arg1="Hello,", arg0="World!")