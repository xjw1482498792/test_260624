import sys, gc
sys.stdout.reconfigure(encoding="utf-8")   # Windows 控制台强制 UTF-8,避免中文乱码

print("=" * 50)
print("演示 1:引用计数 —— 有几个名字指向对象")
print("=" * 50)

a = []                       # 造一个列表对象,a 指向它
# getrefcount 本身会临时多算 1 次引用,所以看到的数比真实多 1
print("a 指向列表后,引用数:", sys.getrefcount(a))   # 2 (a + getrefcount临时)

b = a                        # b 也指向同一个列表 → 引用 +1
print("b = a 之后,引用数:  ", sys.getrefcount(a))   # 3

c = a                        # c 又指向它 → 引用 +1
print("c = a 之后,引用数:  ", sys.getrefcount(a))   # 4

del b                        # 删掉 b → 引用 -1
print("del b 之后,引用数:  ", sys.getrefcount(a))   # 3

c = None                     # c 不再指向 → 引用 -1
print("c=None 之后,引用数: ", sys.getrefcount(a))   # 2


print("\n" + "=" * 50)
print("演示 2:引用数归 0 → 对象被立刻销毁")
print("=" * 50)

class Demo:
    def __init__(self, name):
        self.name = name
    def __del__(self):                       # 对象被销毁时自动调用,用来"亲眼看见"回收
        print(f"  >> 对象 [{self.name}] 被销毁了(引用数归0)")

x = Demo("A")                # 造对象,x 指向它(引用数=1)
print("创建了对象 A")
y = x                        # y 也指向(引用数=2)
print("y = x,现在两个名字指向它")
del x                        # 引用数 2→1,还没归0,不销毁
print("del x 后:还有 y 指着,对象还活着")
del y                        # 引用数 1→0,立刻销毁!
print("del y 后:↓")


print("\n" + "=" * 50)
print("演示 3:循环引用 —— 引用计数的死角")
print("=" * 50)

class Node:
    def __init__(self, name):
        self.name = name
        self.partner = None
    def __del__(self):
        print(f"  >> 节点 [{self.name}] 被回收")

gc.disable()                 # 先关掉垃圾回收器,只看引用计数的表现
n1 = Node("甲")
n2 = Node("乙")
n1.partner = n2              # 甲 指向 乙
# print(sys.getrefcount(n1))
# print(sys.getrefcount(n2))
n2.partner = n1              # 乙 指向 甲  → 两人互相抱住!
del n1
del n2                       # 删掉外部名字,但甲乙还互相引用着,引用数都不为0
print("已 del n1、n2,但它俩互相引用,引用计数无法归0 → 没被回收(上面没有打印销毁)")

print("\n现在手动启动垃圾回收器 gc.collect() ...")
gc.collect()                 # 垃圾回收器出动,检测到这对"孤岛",强制回收
print("↑ 垃圾回收器发现了这对循环引用并清除了它")
