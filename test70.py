#迭代器，生成器，装饰器

#######迭代器
# list1 = [1,2,3]
# iter1 = iter(list1)
# print(next(iter1))
# print(next(iter1))

# class counter():
    
#     def __init__(self, init_value):
#         self.init_value = init_value
#         self.cur_value = None

#     def __iter__(self):
#         return self
    
#     def __next__(self):
#         if self.init_value <= 5:
#             self.cur_value = self.init_value
#             self.init_value += 1
#             return self.cur_value
#         else:
#             raise StopIteration

# c1 = counter(1)
# iter_c1 = iter(c1)
# for tmp in iter_c1:
#     print(tmp)        

#####生成器
# def gen1(number):
#     begin = 1
#     while begin <= number:
#         yield begin
#         begin += 1        

# iter2 = gen1(5)  
# for item in iter2:
#     print(item)
# print(next(iter2))
# print(next(iter2))


#装饰器

def decorate1( num):
    def decorate(ori):
        def wrapper(*args, **kwargs):
            print("before")
            print(args[0])
            for _ in range(num):
                print(ori(*args, **kwargs))
            print("after")
        return wrapper    
    return decorate
@decorate1(3)
def origin(name):
    return "my name is " + name

origin("zhangsan")    