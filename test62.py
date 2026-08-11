from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        new_nums = self.my_sort(nums)
        return new_nums[k - 1]

    def my_sort(self, nums)->list:

        if len(nums) == 1:
            return nums

        half  = len(nums) // 2
        left  = self.my_sort(nums[0:half])
        right = self.my_sort(nums[half:])

        i = j = 0
        my_nums = []
        while i < len(left) and j < len(right):
            if left[i] > right[j]:
                my_nums.append(left[i])
                i += 1
            else:
                my_nums.append(right[j])
                j += 1

        if i == len(left):
            my_nums.extend(right[j:])
        else:
            my_nums.extend(left[i:])    

        return my_nums
        # list1 = [0 for _ in range(k)]
        # print(list1)
        # print(3 // 2)
        # 4 // 2 = 2
        # 3 // 2 = 1
        # 2 // 2 = 1
        # 1 // 2 = 0

res = Solution().findKthLargest([1,2,3,4,5], 2)        
print(res)