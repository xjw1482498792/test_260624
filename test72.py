#闭包
def outer(init, max):
    def inner():
        nonlocal init
        while init < max:
            init += 1
            return(init)
            
    return inner

i = outer(0,5)
print(i())
print(i())

#with原理
a = lambda x : x + 1
# print(a(3))
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(2) as p:
    p.submit(print,a(3))

    # ThreadPoolExecutor.e
