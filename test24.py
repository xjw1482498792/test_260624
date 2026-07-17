from typing import List


class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        #最终结果    
        min_path = list(list())
        for i in range(len(triangle)):
            tmp_row = []
            for j in range(len(triangle[i])):
                if i == 0:
                    tmp_row.append(triangle[0][0])                    
                if i == 1:
                    tmp_row.append(triangle[0][0] + triangle[i][j])                    
                #     2      ->索引 0
                #    3 4     ->    0 1 
                #   6 5 7    ->   0 1 2
                #  4 1 8 3   ->  0 1 2 3
                if i > 1:
                    if j == 0:
                         tmp_row.append(triangle[i][j] + min_path[i - 1][j])
                    elif j < len(triangle[i]) - 1:
                         left  = triangle[i][j] + min_path[i - 1][j - 1]                          
                         right = triangle[i][j] + min_path[i - 1][j]
                         tmp_row.append(min(left, right))                         
                    else:
                         tmp_row.append(triangle[i][j] + min_path[i - 1][j - 1])
            min_path.append(tmp_row)

        # last_line = min_path.pop()    
        # min_result = last_line.pop()
        # for tmp in last_line:
        #     min_result = min(min_result, tmp)
        
        return   min(min_path[len(min_path) - 1])  

print(Solution().minimumTotal([[2],[3,4],[6,5,7],[4,1,8,3]]))

print([i for i in range(3)])

n = 3
print([[0] * n for _ in range(n)])

list1 = [[0] * n for _ in range(n)]
list1[1][0] = 444

for i in range(1,1):
    print("!!!!!")


# class Solution:
#     def minimumTotal(self, triangle: List[List[int]]) -> int:
#         n = len(triangle)
#         f = [[0] * n for _ in range(n)]
#         f[0][0] = triangle[0][0]

#         for i in range(1, n):
#             f[i][0] = f[i - 1][0] + triangle[i][0]
#             for j in range(1, i):
#                 f[i][j] = min(f[i - 1][j - 1], f[i - 1][j]) + triangle[i][j]
#             f[i][i] = f[i - 1][i - 1] + triangle[i][i]
        
#         return min(f[n - 1])

# print(Solution().minimumTotal([[1], [2, 3]]))