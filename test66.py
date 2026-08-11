from typing import Counter, List


class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        index = 0
        tree_nums = 0
        dict1 = Counter()#类型：个数
        for fruit in fruits:
            #进入滑块
            dict1[fruit] += 1
            # if len(dict1) <= 2:
                #符合两种类型
                # tree_nums = max(tree_nums, sum(dict1.values()))
                # continue

            while len(dict1) > 2:
                cur = fruits[index]
                dict1[cur] -= 1
                if dict1[cur] == 0:
                    del dict1[cur]
                index += 1

            tree_nums = max(tree_nums, sum(dict1.values()))    
        return tree_nums

res = Solution().totalFruit([3,3,3,1,2,1,1,2,3,3,4])    
print(res)            
