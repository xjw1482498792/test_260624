# class Person:
#     def __init__(self, name2):
#         self._name2 = name2

#     @property
#     def name(self):
#         return self._name2

# person = Person("小明")

# person._name2 = "XH"
# print(person.name)    # 正确，像访问属性
# print(person._name2)    # 正确，像访问属性
# # print(person.name())  # 错误，name 返回的是字符串    

class Person:
    def __init__(self, age):
        self.age = age  # 会调用下面的 setter

    def set_age(self, value):
        if not isinstance(value, int):
            raise TypeError("年龄必须是整数")

        if value < 0 or value > 150:
            raise ValueError("年龄必须在 0～150 之间")

        self._age = value

    # @property
    # def age(self):
    #     return self._age

    # @age.setter
    # def age(self, value):
    #     if not isinstance(value, int):
    #         raise TypeError("年龄必须是整数")

    #     if value < 0 or value > 150:
    #         raise ValueError("年龄必须在 0～150 之间")

    #     self._age = value

person = Person(18)

print(person.age)  # 像普通属性一样读取：18

person.age = 25    # 像普通属性一样赋值
print(person.age)  # 25

person.age = -10   # ValueError        