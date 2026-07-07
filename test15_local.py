# import threadingd

# dic1 = {"name": "zhangsan", "age": 13}
# print(f'origin: {dic1}')

# del dic1["age"]
# print(f'del: {dic1}')

# dic2 = {"name": "lisi", "age": 14}
# dic1.update(dic2)
# print(f'update: {dic1}')

#元组/列表/集合/字典相关操作
# dic_sort = {"k1": 1, "k2": 2, "k3": 3}
# iter1 = iter(dic_sort)
# print(next(iter1))
# print(next(iter1))

# list1 = list(dic_sort.items())
# print(list1)

#元组
tup1 = (1, 2, 'A')
print(f'tup1: {tup1}')
#元素出现的次数和坐标
print(f"Count of 'A' in tup1: {tup1.count('A')}")#on
print(f"Index of 'A' in tup1: {tup1.index('A')}")#on

#列表
list1 = [1, 2, 'A']
print(f'list1: {list1}')
#增删改查
#增
list1.append('B')
print(f'list1 after append: {list1}')#o1
list1.extend(['C', 'D'])
print(f'list1 after extend: {list1}')#o1
list1.insert(0,'X')
print(f'list1 after insert: {list1}')#on
#删
list1.remove('B')#on
print(f'list1 after remove: {list1}')
list1.pop()#O1
print(f'list1 after pop: {list1}')
list1.pop(0)#On
print(f'list1 after pop(0): {list1}')
#改
list1[0] = 'Y'#On
print(f'list1 after change: {list1}')
list1[1:3] = ['Z', 'W']#On
print(f'list1 after change slice: {list1}')
#查
print(f'list1[0]: {list1[0]}')#O1
print(f'list1[1:3]: {list1[1:-1]}')#On
print(f'list1[-1]: {list1[-1]}')#O1
print(f'list1.index("Z"): {list1.index("Z")}')#On
print(f'list1.count("W"): {list1.count("W")}')#On
print(f'list1 in "W": {"W" in list1}')#On
#清空
list1.clear()#O1
print(f'list1 after clear: {list1}')

#集合
set1 = {1, 2, 'A'}
print(f'set1: {set1}')
#增
set1.add('B')#O1
print(f'set1 after add: {set1}')
set1.update({'C', 'D'})#On
print(f'set1 after update: {set1}')
#删
set1.remove('B')#O1
print(f'set1 after remove: {set1}')
set1.pop()#O1
print(f'set1 after pop: {set1}')
#清空
# set1.clear()#O1
# print(f'set1 after clear: {set1}')
#改
a = {1, 2, 3}
b = {3, 4, 5}
print(f'a: {a}, b: {b}')
# a.update(b)#并集
# print(f'a after update with b: {a}')
# a.intersection_update(b)#交集
# print(f'a after intersection_update with b: {a}')
# a.difference_update(b)#差集
# print(f'a after difference_update with b: {a}')
# a.symmetric_difference_update(b)#对称差集
# print(f'a after symmetric_difference_update with b: {a}')
# c = a | b#并集
# print(f'c (a | b): {c}')
# d = a & b#交集
# print(f'd (a & b): {d}')
# e = a - b#差集
# print(f'e (a - b): {e}')
# f = a ^ b#对称差集
# print(f'f (a ^ b): {f}')
#查
print(f'1 in a: {1 in a}')#On

#字典
dict1 = {"name": "zhangsan", "age": 13}
print(f'dict1: {dict1}')

#增
dict1["gender"] = "male"#O1
print(f'dict1 after add: {dict1}')
#改
dict1["age"] = 14#O1
print(f'dict1 after change: {dict1}')
#删
dict1.pop("gender")#O1
print(f'dict1 after pop: {dict1}')
#查
dict1.get("name")#O1
print(f'dict1.get("name"): {dict1.get("name")}')
dict1.get("key", "default")#O1
print(f'dict1.get("key", "default"): {dict1.get("key", "default")}')
age = dict1['age']
print(f'dict1["age"]: {age}')
#其他删
dicta = {"name": "lisi", "age": 14}
dictb = {"name": "wangwu", "age": 15, "gender": "female"}
# dl = dicta.popitem()#删除最后一个
# print(f'dicta after popitem: {dicta}, popped item: {dl}')
dicta.update(dictb)#O(n)#更新
print(f'dicta after update with dictb: {dicta}')
del dicta["gender"]#O1
print(f'dicta after del "gender": {dicta}')
dicta.clear()#O1
print(f'dicta after clear: {dicta}')

#验证字典顺序
dict_sorted = {"a": 1, "b": 2, "c": 3}
print(f'dict_sorted: {dict_sorted}')
for key, value in dict_sorted.items():
    print(f'key: {key}, value: {value}')
print(f'type of dict_sorted: {type(dict_sorted.items())}')


#总结
#元组 列表 集合 字典
#元组
tuple1 = (1, 2, 3)#增删改都不行
print(f'tuple1.count(1): {tuple1.count(1)}') #求次数
print(f'tuple1.index(2): {tuple1.index(3)}') #求坐标
if 1 in tuple1:#求是否包含
    print("1 is in tuple1")
#列表
list1 = [1, 2, 3]
list1.append(4)#增
print(f'list1 after append: {list1}')
list1.remove(4)#删
print(f'list1 after remove: {list1}')
list1[0] = 0#改
print(f'list1 after change: {list1}')
#集合
set1 = {1, 2, 3}
set1.add(4)#增
print(f'set1 after add: {set1}')
set1.remove(4)#删
print(f'set1 after remove: {set1}')
#字典
dict1 = {"a": 1, "b": 2, "c": 3}
dict1["d"] = 4#增
print(f'dict1 after add: {dict1}')
del dict1["d"]#删
print(f'dict1 after del: {dict1}')

#线程池
# from concurrent.futures import ThreadPoolExecutor
# from time import sleep


# def download_img(url):
#     sleep(1)
#     return f'{url} download complete'

# with ThreadPoolExecutor(2) as executor:
#     results = executor.map(download_img, [f'url_{i}' for i in range(10)])

# for result in results:
        # print(result)