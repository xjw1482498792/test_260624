def outer():
    name = "小明"

    def inner():
        print(name)

    return inner

outer()()