class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        # -7, -3, 0, 1, 3, 4, 5
        set1 = set()
        res = []
        nums.sort()
        #不够一组
        if len(nums) < 3:
            return []
        
        #计算
        index_a = 0
        index_b = 1
        index_c = len(nums) - 1
        while index_a <= len(nums) - 3:
            total = nums[index_a] + nums[index_b] + nums[index_c]
            if  total == 0:
                tmp = (nums[index_a], nums[index_b], nums[index_c])
                set1.add(tmp)
                index_b += 1
                index_c -= 1
            elif total < 0:
                index_b += 1
            else:
                index_c -= 1    

            if index_b >= index_c:
                index_a += 1
                index_b = index_a + 1
                index_c = len(nums) - 1
           


        for tup_tmp in set1:
            res.append(list(tup_tmp))
        return res
    
print(Solution().threeSum([-1, 0, 1, 2, -1, -4])   )