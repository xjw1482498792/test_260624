# from functools import cache
# from typing import List

# class Solution:
#     def countRoutes(
#         self,
#         locations: List[int],
#         start: int,
#         finish: int,
#         fuel: int
#     ) -> int:
#         MOD = 10**9 + 7
#         n = len(locations)

#         @cache
#         def dfs(city, remain):
#             # 可以在当前城市结束路线
#             routes = 1 if city == finish else 0

#             for next_city in range(n):
#                 if next_city == city:
#                     continue

#                 cost = abs(
#                     locations[city] - locations[next_city]
#                 )

#                 if cost <= remain:
#                     routes += dfs(next_city, remain - cost)

#             return routes % MOD

#         return dfs(start, fuel)
# print(Solution().countRoutes([1, 2, 3], 0, 2, 4)        )


# # 1 2 3
# # 0 1 2
# #（坐标）
# #第一步： （1，3）（2，2）
# #第二步； （0，2）（2，2）（1，1）
# #第三步：  （1，1）（2，0）（1，1）（0，0）(0,0)(2,0)
# #第四步：  (2,0)(2,0)

# #0->2
# #0->1->2
# #0->1->0->2
# #0->2->1->2
# #

# #  1   2   3 #从s=0到f=2，fuel=4
# #  0->2
# #  0->1->2
# #  0->2->1->2
# #  0->1->2->1->2
# #  0->1->0->2
# #  0->1->0->1->2


class Solution:
    def countRoutes(self, locations: List[int], start: int, finish: int, fuel: int) -> int:
#纵列标识油，横排标识方式集中，从4出发
#第一轮和第二轮差别，完成用完油，在第一轮基础上加油
#         0  1  2  3  4  5  6  7  8  9
#   0     0  1  0  0  0  0  0  0  0  0     
#   1     1  0  1     
#   2     0  2  0  1
#   3     1  0  2  0  1
#   4     0  2  0  2  0  1     
#   5     1  0  2  0  2  0  1  
#   1->2->3   ###1*2*1=2
#   1->2->3->4->3     ###  
#   1->2->3->5->3     
# 
# 从3走去8
# 按油走不太行，按步走吧
#       2   3   6   8    4
#  0        1   
#  1    1       1   1    1
#  2        1   1   1    1
#  3   
#  第一步 记录当前location和剩余fuel，记录所有落点
#  第二步 从第一步的落点走，记录当前location和剩余fuel，记录所有落点
#  最后一步，记录所有落点
#  统计每步落点在finish的所有落点，求和就是结果
#  落点（步，位置，值，剩余fuel）步0 位置1 值3 剩余5
        tuple0 = (0, 1, 3, 5)
        tuple1 = (1, 0, 2, 4),(1, 2, 6, 2),(1, 3, 5, 0),(1, 4, 4, 4)
        tuple2 = ()

        num = 0
        stack1 = list()
        stack1.append((start, locations[start], fuel))

        while stack1:
                tuple_pop = stack1.pop()
                #找出入栈的其他元组 和 到达finish的元组
                if tuple_pop[0] == finish:
                    num += 1
                for i,v in enumerate(locations):
                    if tuple_pop[0] == i:
                        continue
                    need_fuel = abs(tuple_pop[1] - v)#值的比较
                    remain = tuple_pop[2] - need_fuel#fuel的比较
                    #剩余油量>=0还不够，
                    if remain >= abs(locations[finish] - v ):
                        #入栈
                        tuple_append = (i, v, remain)#位置，值，剩余fuel
                        stack1.append(tuple_append)


            
        return num   