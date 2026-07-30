#迭代器

list1 = list([1,3,5])

iter1 = iter(list1)
print(next(iter1))
# print(next(iter1))
# print(next(iter1))


def fun_gen():
    count = 0
    while True:
        yield count
        count += 2

iter2 = fun_gen()

print(next(iter2))  
print(next(iter2))  


set1 = set({1,3})
set1.add(2)
set1.remove(1)
print(set1)


list8 = list()
list8.append(8)
list8.append(7)
list8.remove(8)
# del list8[1]
print(list8)