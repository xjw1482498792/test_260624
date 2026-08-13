# def climb(n: int):

#     if n == 1:
#         return 1
#     if n == 2:
#         return 2    


#     return climb(n - 1) + climb(n - 2)

# print(climb(3))


#----------------------------------
# from typing import Counter


# def get_max(arr: list, top: int):
#     dict1 = Counter(arr)
#     # for tmp in arr:
#     #     dict1[tmp] += 1
#     # print("hello world".split(" "))
#     return [ tmp[0] for tmp in dict1.most_common(top)]

#----------------------------------
def get_max(arr: list, top: int):
    dict1 = {}
    for tmp in arr:
        if tmp in dict1:
            dict1[tmp] += 1
        else:
            dict1[tmp] = 1    

    list1 = list(dict1.items()     )
    list1.sort(key=lambda x: x[1], reverse=True)
    return [ tmp[0] for tmp in list1[:top]]

print(get_max([2,2,3,1,1,1], 2))     