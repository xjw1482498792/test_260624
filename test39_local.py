#split
str1 = " 你好 我的名字是阿伟（awei——2）(awei)"
list1 = str1.split("(")
list2 = str1.split("(")[0].split("（")
list3 = str1.split("(")[0].split("（")[0].strip()
print(list1)
print(list2)
print(list3)

#函数参数
def fun1(arg0, arg1, arg2=2, arg3=3):
    print(f'arg0:  {arg0}')
    print(f'arg1:  {arg1}')
    print(f'arg1:  {arg2}')
    print(f'arg1:  {arg3}')

fun1(0,1,  5)    

#other
kwargs = {"key1": "value1", "key2": "value2"}
# def fun2( **kwargs):
args = ("A","B","C")
list1 = ("c","b","a")
def fun2(*args, **kwargs):
    print(args)
    print(kwargs)
# fun2(**kwargs)    
fun2(*list1,**kwargs)  


#or
a = None
# print(a or "world")
print(a)