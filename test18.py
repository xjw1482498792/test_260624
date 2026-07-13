from typing import List


class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        #固定1和2 3和4相互靠近指针
        res = []
        nums.sort()
        # index_4 = len(nums) - 1
        for tmp1 in range(len(nums) - 3):
            if tmp1 > 0 and nums[tmp1] == nums[tmp1 - 1]:
                continue
            for tmp2 in range(tmp1 + 1, len(nums) - 2):
                if tmp2 > tmp1 + 1 and nums[tmp2] == nums[tmp2 - 1]:
                    continue
                index_4 = len(nums) - 1
                for tmp3 in range(tmp2 + 1, len(nums) - 1):
                    if tmp3 > tmp2 + 1 and nums[tmp3] == nums[tmp3 - 1]:
                        continue

                    while index_4 > tmp3 and nums[tmp1] + nums[tmp2] + nums[tmp3] + nums[index_4] > target:
                        index_4 -= 1
                    if tmp3 == index_4:
                        break
                    if nums[tmp1] + nums[tmp2] + nums[tmp3] + nums[index_4] == target:
                        res.append([nums[tmp1], nums[tmp2], nums[tmp3], nums[index_4]]) 
                   

        return res         

print(Solution().fourSum([1,0,-1,0,-2,2],0))                   
