from typing import List


# class Solution:
#     def minSubArrayLen(self, target: int, nums: List[int]) -> int:
#         sum_all = sum(nums)

#         if sum_all < target:
#             return 0

#         left = right = 0
#         total = nums[0]
#         min_count = len(nums)
#         while True :
#             while total < target and right < len(nums) - 1:
#                 right += 1
#                 total += nums[right]

#             if total >= target:
#                 min_count = min(min_count, right - left + 1)    
                
#             while total >= target and left < right:                
#                 total -= nums[left] 
#                 left += 1
                  
#                 if total >= target:
#                     min_count = min(min_count, right - left + 1) 

#             if (right == len(nums) - 1) or min_count == 1:
#                 return min_count       


# class Solution:
#     def minSubArrayLen(self, s: int, nums: List[int]) -> int:
#         if not nums:
#             return 0
        
#         n = len(nums)
#         ans = n + 1
#         start, end = 0, 0
#         total = 0
#         while end < n:
#             total += nums[end]
#             while total >= s:
#                 ans = min(ans, end - start + 1)
#                 total -= nums[start]
#                 start += 1
#             end += 1
        
#         return 0 if ans == n + 1 else ans


class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        index = 0
        cur_sum = 0
        res = 0
        for i, num in enumerate(nums):
            cur_sum += num

            #构建滑块
            if target > cur_sum:                
                continue
            
            while target <= cur_sum:      
                res = i - index + 1 if res == 0 else min(res, i - index + 1)          
                cur_sum -= nums[index]
                index += 1
                
        return res        
res = Solution().minSubArrayLen(7,[2,3,1,2,4,3] )    
print(res)

