# 列表推导式
data_list = [x * 2 for x in range(5)]

# 生成器表达式
data_generator = (x * 2 for x in range(5))


print(data_list) 
print(data_generator) 
print(next(data_generator))
print(next(data_generator))