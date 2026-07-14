from typing import List


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        length = len(nums)
        if length == 0:
            return 0
        if length == 1:
            return 0 if target <= nums[0] else 1
        nums.sort()
        for index in range(length):
            if nums[index] == target:
                return index
            if nums[index] > target:                 
                return index
        return length    
    
# print(Solution().searchInsert([1,2,5], 3))   
# def lower_bound(nums: List[int], target: int) -> int:
#     left, right = 0, len(nums) - 1  # 闭区间 [left, right]
#     while left <= right:  # 区间不为空
#         # 循环不变量：
#         # nums[left-1] < target
#         # nums[right+1] >= target
#         mid = (left + right) // 2
#         if nums[mid] < target:
#             left = mid + 1  # 范围缩小到 [mid+1, right]
#         else:
#             right = mid - 1  # 范围缩小到 [left, mid-1]
#     return left

# def lower_bound3(nums: List[int], target: int) -> int:
#     left, right = -1, len(nums)  # 开区间 (left, right)
#     while left + 1 < right:  # 区间不为空
#         mid = (left + right) // 2
#         # 循环不变量：
#         # nums[left] < target
#         # nums[right] >= target
#         if nums[mid] < target:
#             left = mid  # 范围缩小到 (mid, right)
#         else:
#             right = mid  # 范围缩小到 (left, mid)
#     return right

def lower_bound2(nums: List[int], target: int) -> int:
    left = 0
    right = len(nums) - 1 # 左闭右开区间 [left, right)
    while left <= right:  # 区间不为空
        # 循环不变量：
        # nums[left-1] < target
        # nums[right] >= target
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1  # 范围缩小到 [mid+1, right)
        else:
            right = mid - 1  # 范围缩小到 [left, mid)
    return right  # 或者 right


print(lower_bound2([-4, -3, -2, -1, 0, 1, 2, 3, 4], 0))
# -1 0 1 2 3   target = 1

class Solution:
    def search(self, nums: List[int], target: int) -> int:

        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right ) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left += 1
            elif nums[mid] > target:
                right -= 1    
        return -1        