# with open("test.txt", "r", encoding="utf-8") as file:
#     content = file.read()

# print(content)    


# manager = open("test.txt", "r", encoding="utf-8")
# file = manager.__enter__()

# try:
#     content = file.read()
# finally:
#     manager.__exit__(None, None, None)    

# class Node:
    
#     def __init__(self, val, next):
#         self.val = val
#         self.next = next

# class User:
#     # __slots__ = ("name", "age")

#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

# user = User("小明", 18)

# user.name = "小红"     # 可以
# user.address = "北京"  # AttributeError

# print(user.__dict__)     
# print(user.address)   

#lambda
# from functools import reduce
 
# numbers = [1, 2, 3, 4, 5]

# def fun(x, y):
#     return x+y
 
# # 使用 reduce() 和 lambda 函数计算乘积
# product = reduce(fun, numbers)
# # product = reduce(lambda x, y: x * y, numbers)
 
# print(product)  # 输出：120

# #map and reduce
# numbers = [1, 2, 3, 4]
# set1 = {1,2,3,4}

# result = map(lambda x: x * 2, set1)

# print(result)
# print(list(result))
# # [2, 4, 6, 8]

#反射
class User:
    # __slots__ = ("name", "age")

    def __init__(self, name, age):
        self.name = name
        self.age = age

user = User("小明", 18)        
user.login()              # 普通调用
getattr(user, "login")()  # 反射调用