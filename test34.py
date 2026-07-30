###二分查找
###排序：冒泡还是啥

#查找
#从一个数组，找一个元素，返回坐标
#1，2，3，4，5
import random
from typing import List


def binary_search(nums: list, target: int)->int:
    nums.sort()
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2        
        if nums[mid] == target:
            return mid
        
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


print(binary_search([1,5,6,9,8,7], 8))


#排序
# 1 3 2 7 8 5
#先找出最大的
def sort_list1(nums: list)->list:
    width = len(nums) - 1#表示无序元素最后位置，目前都无序
    
    while width > 0:
        flag = True
        for i in range(width):
            if nums[i] > nums[i + 1]:
                tmp = nums[i]
                nums[i] = nums[i + 1]
                nums[i + 1] = tmp  
                flag = False
        if flag:
            return nums          
        width -= 1              
    return nums

#有序区间
def sort_list2(nums: list)->list:
     #表示有序的边界
    for i in range( 1, len(nums)):
        j = i
        while j > 0 and nums[j] < nums[j - 1]:
                tmp = nums[j]
                nums[j] = nums[j - 1]
                nums[j - 1] = tmp 
                j -= 1   
    return nums                     

#快速排序是啥
# 1 5 3 6 7 4
# class Solution:
#     def sortArray(self, nums: List[int]) -> List[int]:

#         if len(nums) <= 1:
#             return nums

#         pivot = random.choice(nums)
#         left = list()
#         equal = list()
#         right = list()
#         for num in nums:
#             if num < pivot:
#                 left.append(num)
#             elif num == pivot:
#                 equal.append(num)
#             else:
#                 right.append(num)

#         # res = self.sortArray(left)
#         # res.extend(equal)
#         # res.extend(self.sortArray(right))
#         return self.sortArray(left)  + equal + self.sortArray(right)

# class Solution:
#     def sortArray(self, nums: list[int]) -> list[int]:
#         if len(nums) <= 1:
#             return nums

#         mid = len(nums) // 2
#         left = self.sortArray(nums[:mid])
#         right = self.sortArray(nums[mid:])

#         result = []
#         i = j = 0

#         while i < len(left) and j < len(right):
#             if left[i] <= right[j]:
#                 result.append(left[i])
#                 i += 1
#             else:
#                 result.append(right[j])
#                 j += 1

#         result.extend(left[i:])
#         result.extend(right[j:])
#         return result

#手写分治,归并排序
# class Solution:
#     def sortArray(self, nums: List[int]) -> List[int]:
#         mid = len(nums) // 2# (LEN - 1)/ 2
#         # 1      ->0     ->0
#         # 1 2    ->1     ->0
#         # 1 2 3  ->1     ->1
#         if len(nums) <= 1:
#             return nums
        
#         left = self.sortArray(nums[:mid])
#         right = self.sortArray(nums[mid:])

#         res = []
#         i = j = 0
#         while i < len(left) and j < len(right):
#             if left[i] < right[j]:
#                 res.append(left[i])
#                 i += 1
#             else:  
#                 res.append(right[j])
#                 j += 1

#         res.extend(left[i:])
#         res.extend(right[j:]) 

#         return res            

#其他人的快排
# class Solution:
#     def sortArray(self, nums: List[int]) -> List[int]:

#         def quick_sort(arr, low, high):
#             if low >= high:             # 递归结束
#                 return  

#             # 1 5 3 4 2
#             pivot_idx = random.randint(low, high)                   # 随机选择pivot
#             arr[low], arr[pivot_idx] = arr[pivot_idx], arr[low]     # pivot放置到最左边
#             pivot = arr[low]                                        # 选取最左边为pivot

#             left, right = low, high     # 双指针
#             while left < right:
                
#                 while left<right and arr[right] > pivot:            # 找到右边第一个<=pivot的元素【需考虑重复元素问题】
#                     right -= 1
#                 if left < right:
#                     arr[left] = arr[right]                          # 并将其移动到left处
#                     left += 1                                       # left指向下一个待排序的元素
                
#                 while left<right and arr[left] < pivot:             # 找到左边第一个>=pivot的元素【需考虑重复元素问题】
#                     left += 1
#                 if left < right:
#                     arr[right] = arr[left]                          # 并将其移动到right处
#                     right -= 1                                      # right指向下一个待排序的元素
            
#             arr[left] = pivot                   # pivot放置到中间left=right处
            
#             mid = left                          # 以mid=left=right为分割点
#             quick_sort(arr, low, mid-1)         # 递归对mid两侧元素进行排序
#             quick_sort(arr, mid+1, high)
        

#         quick_sort(nums, 0, len(nums)-1)        # 调用快排函数对nums进行排序
#         return nums


#手写快排
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:

        def my_sort(nums: List[int], left: int, right: int):

            if left >= right:
                return

            left_last, right_last = left, right
            rand_idx = random.randint(left, right)
            rand = nums[rand_idx]
            nums[left], nums[rand_idx] = nums[rand_idx], nums[left]

            target = nums[left]

            while left < right:
                while left < right and nums[right] > rand:
                    right -= 1
                if left < right:
                    nums[left] = nums[right]
                    left += 1
                while left < right and nums[left] < rand:
                    left += 1
                if left < right:
                    nums[right] = nums[left]
                    right -= 1

            nums[left] = target

            my_sort(nums, left_last, left - 1)                    
            my_sort(nums, left + 1, right_last)  

        my_sort(nums, 0, len(nums) - 1)        
        return nums              


print(Solution().sortArray([1,5,3,4,2]))
