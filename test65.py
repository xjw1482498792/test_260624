from typing import Counter


dic1 = {}

dic1['A'] = 1

print(dic1)


str1 = "abcc"
dict2 = Counter(str1)
print(dict2)

dic3 = {'A': 1}
print(dic1 == dic3)

dic4 = {1:2,2:4}
print(f'values：{dic4.values()}')
print(sum(dic4.values()))