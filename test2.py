# if (n := len(a)) > 10:
#     print(f"List is too long ({n} elements, expected <= 10)")

# a = 1
# b = 2
    
# print((a>b)-(a<b))
# print("\a")

# print("%#08d" % 10)

# print('abc'.find('a',1,2))

def decorator_function(original_function):
    def wrapper(*args, **kwargs):
        # 调用前
        print("执行前")

        result = original_function(*args, **kwargs)

        # 调用后
        print("执行后")

        return result
    return wrapper

@decorator_function
def target_function():
    print("原函数执行")

