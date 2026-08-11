#__slots__作用，限制实例属性随意添加
class User:
    glb = 345
    __slots__ = ("name", "age")
    def __init__(self, name):
        self.name = name


# print(User.glb)
User.gl2 = 3333
print(User.gl2)
user = User("Tom")
# user.age = 20
# print(user.__dict__)  # {'name': 'Tom'}

#高级函数map
# print(list(map(lambda x: x*x, [1,2,3])))
iter1 = map(lambda x: x*x, [1,2,3])
# for tmp in iter1:
#     print(tmp)  
# print(type(iter1))
print(next(iter1))
print(next(iter1))
