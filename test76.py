class Person:
    def __init__(self, age):
        self.age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("年龄必须是整数")
        if value < 0 or value > 150:
            raise ValueError("年龄范围不合法")

        self._age = value

    @age.deleter
    def age(self):
        del self._age

person = Person(20)

print(person.age)  # 实际调用 getter
person.age = 25    # 实际调用 setter
del person.age     # 实际调用 deleter        