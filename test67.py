from typing import Counter


class Solution:
    def countGoodSubstrings(self, s: str) -> int:
        dic1 = Counter()
        res = 0
        for i,war in enumerate(s):
            dic1[war] += 1
            if sum(dic1.values()) < 3:
                continue

            if sum(dic1.values()) > 3:                
                dic1[s[i - 3]] -= 1
                if dic1[s[i - 3]] == 0:
                    dic1.pop(s[i - 3])

            if len(dic1) == 3:   
                res += 1
        return     res    
 
res  = Solution().countGoodSubstrings("aababcabc")  
print(res)             
