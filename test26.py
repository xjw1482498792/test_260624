
# class Solution:
#     def uniquePaths(self, m: int, n: int) -> int:
#         #高3  长7 =>向下走两步，向右走6步
#         #一共走8步
#         #模型全是1，有两步给2
#         # 1 1 1 1 1 1 1 1
#         # 2 2 1 1 1 1 1 1
#         # 7 + 6 + ... + 1
#         # C8 2 
#         big = m + n - 2
#         small = min(n, m) - 1
#         #从big里面选small有多少种
#         sum_son = 1
#         sum_parent = 1
#         for i in range(small) :
#             sum_son *= big 
#             big -= 1
#             sum_parent *= (i + 1) 
#         return int(sum_son / sum_parent)
#         print(sum_son)    
#         print(sum_parent)    
# # 分子  6 * 5
# # 分母  2 * 1
# print(Solution().uniquePaths(2, 3)       
# 
#      )


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        #     1 2 3 4 5

        # 1   1 1 1 1
        # 2   1 2 3 4
        # 3   1 3 6 10
        # 4   1 4 1020
        list1 = [1] * m #m列
        list2 = [list1] * n #n行
        for i in range(n):
            for j in range(m):
                if i == 0 or j == 0:
                    list2[i][j] = 1
                else:
                    list2[i][j] = list2[i - 1][j] + list2[i][j - 1]
        return list2[n - 1][m - 1]
    
print(Solution().uniquePaths(3, 7)    )