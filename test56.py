#多继承
# class A:
#     def show(self):
#         print("A")


# class B(A):
#     def show(self):
#         print("B")


# class C(A):
#     def show(self):
#         print("C")


# class D(B, C):
#     pass

# D().show()
# print(D.mro())


#super
class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, score):
        super().__init__(name)
        self.score = score


student = Student("小明", 95)

print(student.name)   # 小明
print(student.score)  # 95