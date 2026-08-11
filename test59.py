# from abc import ABC, abstractmethod


# class Animal(ABC):
#     @abstractmethod
#     def speak(self):
#         pass


class Dog:
    def speak(self):
        print("汪汪")


class Cat:
    def speak(self):
        print("喵喵")


class Person:
    def speak(self):
        print("你好")


def make_sound(obj):
    obj.speak()

make_sound(Dog())     # 汪汪
make_sound(Cat())     # 喵喵
make_sound(Person())  # 你好    