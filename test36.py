class Cat:

    def __new__(cls, *args, **kwargs):
        print("newing*****")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, *args, **kwargs):
        self.name = args
        self.all = kwargs

    def __eq__(self, value):
        return True if self.name == value else False

    def speak(self):
        print(self.name)   
        print(self.all)

Cat("xj", a = 'a', b = 'b').speak()  

# print(Cat("xm") == ("xma",))
    