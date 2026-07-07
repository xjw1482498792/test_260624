class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        # -7, -3, 0, 1, 3, 4, 5
        set1 = set()
        res = []
        nums = sorted(nums)
        #不够一组
        if len(nums) < 3:
            return []        
        #计算
        # index_a = 0
        # index_b = 1
        # index_c = 2
        # while True:
        #     if nums[index_a] + nums[index_b] + nums[index_c] == 0:
        #         tmp = (nums[index_a], nums[index_b], nums[index_c])
        #         set1.add(tmp)
        #     index_c += 1
        #     if index_c == len(nums):
        #         index_b += 1        
        #         index_c = index_b + 1
        #     if index_b == len(nums) - 1:
        #         index_a += 1
        #         index_b = index_a + 1
        #         index_c = index_b + 1
        #     if index_a == len(nums) - 2:
        #         break
        index_a = 0
        index_b = 1
        index_c = len(nums) - 1
        while True:
            if nums[index_a] + nums[index_b] + nums[index_c] == 0:
                tmp = (nums[index_a], nums[index_b], nums[index_c])
                set1.add(tmp)
                
            index_c += 1
            if index_c == len(nums):
                index_b += 1        
                index_c = index_b + 1
            if index_b == len(nums) - 1:
                index_a += 1
                index_b = index_a + 1
                index_c = index_b + 1
            if index_a == len(nums) - 2:
                break        


        for tup_tmp in set1:
            res.append(list(tup_tmp))
        return res
              
            

#每一组不能重复，怎么实现，外层用集合，内层用什么
tup1 = (1, 2, 3)
tup2 = (1, 3, 2)
print(tup1 == tup2)

print(Solution().threeSum([-1, 0, 1, 2, -1, -4])                        )