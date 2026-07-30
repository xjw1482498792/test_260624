#深拷贝 浅拷贝 赋值

# a = 1
# b = a

# print(a is b)

import copy

# a = [[1,2],[3,4]]
# b = copy.copy(a)

# print(a[1] is b[1])

# a = [[1,2],[3,4]]
# b = copy.deepcopy(a)

# print(a[1] is b[1])


#LEGB是啥
# x = "Global"

# def outer():
#     x = "Enclosing"

#     def inner():
#         x = "Local"
#         print(x)

#     inner()

# outer()

#nonlocal
# def outer():
#     count = 0

#     def inner():
#         nonlocal count
#         count += 1

#     inner()
#     print(count)

# outer()  # 1

number = 10
count = 0

def outer():
    count = 20

    def inner():
        global number
        nonlocal count

        number += 1  # 修改模块全局变量
        count += 1   # 修改外层函数变量
        print(number)     
        print(count)
    inner()    

outer()             