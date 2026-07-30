# class Solution:
#     def lastRemaining(self, n: int) -> int:
#         #递归删除，最后剩一个元素
#         list1 = [num + 1 for num in range(n)]
#         set1 = set(list1)
#         cur = 1
#         jump = 2
#         flag = True#正向
#         while len(set1) > 1:
#             if flag:
#                 if cur in set1:
#                     set1.remove(cur)
#                     cur += jump
#                 elif cur - jump // 2 in set1:
#                     cur = cur - jump // 2
#                     jump *= 2
#                     flag = False
#                 else:
#                     cur = cur - jump - jump // 2
#                     jump *= 2    
#                     flag = False
#             else:
#                 if cur in set1:
#                     set1.remove(cur)
#                     cur -= jump
#                 elif cur + jump // 2 in set1:
#                     cur = cur + jump // 2
#                     jump *= 2
#                     flag = False
#                 else:
#                     cur = cur + jump + jump // 2
#                     jump *= 2    
#                     flag = False                            
#         return set1.pop()


class Solution:
    def lastRemaining(self, n: int) -> int:
        a1 = 1
        k, cnt, step = 0, n, 1
        while cnt > 1:
            if k % 2 == 0:  # 正向
                a1 += step
            else:  # 反向
                if cnt % 2:
                    a1 += step
            k += 1
            cnt >>= 1
            step <<= 1
        return a1

print(Solution().lastRemaining(9))


# 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15

# 1-1
# 2-2
# 3-2
# 4-2
# 5-2
# 6-4
# 7-4
# 8-6
# 9-6
# 10-8
# 11-8
# 12-10
# 13-10
# 14-12
