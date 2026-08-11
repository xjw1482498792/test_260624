# 列表推导式
numbers = [x * 2 for x in range(10)]
print(numbers)

# 生成器表达式
numbers = (x * 2 for x in range(10))
print(next(numbers))