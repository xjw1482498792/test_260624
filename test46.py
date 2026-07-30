#GLOBAL NONLOCAL

num1 = 100
num2 = 200

def fun1():
    # global num1
    # nonlocal num1
    num1 = 10
    num2 = 20
    def fun2():
        # global num1
        # nonlocal num1
        num1 = 1
        num2 = 2
        print(num1, num2)
     
    fun2()
    print(num1, num2)   
    


fun1()
print(num1, num2)

#闭包
def fun3(init):
    
    def fun4():
        nonlocal init
        init += 1
        return init
    return fun4

print("bibao")
fun4 = fun3(0)
print(fun4())
print(fun4())

#异常
print("=--------------")
def fun6():
    try:
        return
        i1 = 1/0
    except:
        print("ERROR")    
    finally:
        print("FINNALLY")    


fun6()