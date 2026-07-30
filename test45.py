from typing import List

# class Node:
        
#         def __init__(self, val = 0, next = None):
#               self.val= val
#               self.next = next
            
        

# class Solution:


#     def maxSubArray(self, nums: List[int]) -> int:
#         list1 = []
#         last = 0
#         for num in nums:
#             if not list1:
#                 list1.append(num)
                
#             elif last * num >= 0:
#                 tmp = list1.pop()
#                 list1.append(tmp + num)
#             else:
#                 list1.append(num)    

#             last = num  
#         #已经变成一正一负
#         res = float('-inf')
#         flag = False
#         tmp_slow = 0
#         tmp_fast = 0
#         for l1 in list1:
#             if not flag:
#                 if l1 < 0:
#                     continue
#                 else:
#                     flag = True
#                     tmp_slow += l1
#                     # res = max(res, tmp)

#             else:
#                 if l1 < 0:
#                     tmp_fast = tmp_slow + l1
#                 else:
#                     tmp_fast += l1
#                     if tmp_fast >= tmp_slow:
#                         tmp_slow = tmp_fast
#                         tmp_fast = 0
#                     else:
#                         flag = False
#                         res = max(res, tmp_slow)
#                         tmp_slow = tmp_fast = 0

#         print(list1)
#         return res

class Solution:


    def maxSubArray(self, nums: List[int]) -> int:
        my_list = []
        for num in nums:
            if not my_list:
                my_list.append(num)
                last = num
                continue
            last = max(last + num, num)
            my_list.append(last)
        return max(my_list)

# -2 1 -3 4 -1 2 1 -5 4
# -2
# 1
# -2
# 4
# 3
# 5                           

    
        

print(Solution().maxSubArray([-2,1,-3,4,-1,2,1,-5,4]))  
# -2 1 -3 4 -1 2 1 -5 4
# -2 1 -3 4 -5 3 -5 1000