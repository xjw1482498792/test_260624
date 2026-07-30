class Person:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"大家好，我是{self.name}")


person = Person("小明")

# 1. hasattr：判断对象是否有指定属性或方法
print(hasattr(person, "name"))       # True
print(hasattr(person, "say_hello"))  # True

# 2. getattr：通过字符串获取属性
name = getattr(person, "name")
print(name)  # 小明

# 通过字符串获取并调用方法
method = getattr(person, "say_hello")
method()  # 大家好，我是小明

# 3. setattr：通过字符串设置属性
setattr(person, "age", 18)
print(person.age)  # 18

# 4. delattr：通过字符串删除属性
delattr(person, "age")
print(hasattr(person, "age"))  # False

#no
if command == "login":
    user.login()
elif command == "logout":
    user.logout()

#yes
method = getattr(user, command)
method()    
