#join 链接一个可迭代对象
list1 = [1,2,3,4,5]
print(f'list1={ list1 }')

list2 = ["a", "b", "c", "d", "e"]
list2 = '+'.join(list2)
print(list2)
print(type(list2))

#zip 合并两个可迭代对象
lista = [1,2,3]
listb = ["张三", "李四", "王五"]

res = "----".join( f'{id}-{name}' for id, name in zip(lista, listb))
print(f'res：{res}')


list_dict = [{"A","a"},{"B","b"},{"C","c"}]
for i, j in list_dict:
    print(f'i-j={ i }-{ j }')