import asyncio

#演示嵌套await
async def fun1():
    print("fun1 start")
    await asyncio.sleep(2)
    print("fun1 end")

async def fun2():
    await fun1()

async def fun3():
    print("fun1 start")
    await asyncio.sleep(2)
    print("fun1 end")    

async def main():
    # await asyncio.gather(fun2(), fun3())
    await fun2()
    await fun3()

# asyncio.run(fun2())     
asyncio.run(main())
