def print_num():
    i = 0
    while i < 5:
        yield i
        i += 1

gen1 = print_num()

# for i in  gen1:
#     print(i)
# 
print(next(gen1))  # Output: 0
print(next(gen1))  # Output: 1
print(next(gen1))  # Output: 2