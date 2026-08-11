from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "汪汪"


dog = Dog()
print(dog.speak())    


from concurrent.futures import ThreadPoolExecutor
#    ThreadPoolExecutor.__