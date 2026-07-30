#字符串反转
str1 = "abcdefg"
str2 = str1[0:4:1]
str3 = str1[4::-1]
print(str3)

#手写迭代器
list1 = [1,2,3,4]
iter1 = iter(list1)

print("迭代器")
print(next(iter1))
print(next(iter1))

#手写生成器
print("生成器")
def gen1():
    i = 7
    while i > 0:
        yield i
        i -= 1

iter2 = gen1()        
print(next(iter2))        
print(next(iter2))        


#手写装饰器
print("装饰器")
def decor1(origin_function):
    def warper(*args, **kwargs):
        print("decorating1")
        print(origin_function(*args, **kwargs))
        print("decorating2")
    return warper

# print(list)

@decor1
def origin(name: str)-> str:
    return f'我的名字是：{ name }'


origin("xm")

# print(origin("X-H"))
# print(origin("X-H"))




# def fun3( *args, **kwargs):
#     print(args)
#     print(kwargs)




# print("test-----------------")
# fun3(12, B = 2,A = 1,)   
# tuple1 = (1) 
# print(type(tuple1))
# print(type(origin))



# class Cat():
    
#     def __init__(self, name):
#         self.name = name

#     def speak(self):
#         print(self.name)

# def fun1():
#     print("")

# cat1 = Cat("MIMI")    

# print("type------------------------")
# print(type(cat1))
# print(type(fun1))
# from types import FunctionType 
# print(type(Cat))
# print(type(FunctionType))

# Cat("xiaomao").speak()   

# def fun2(cat1: Cat):
#     cat1.speak()

# fun2(Cat("xm"))    