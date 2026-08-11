from typing import List


class Solution:
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        # first = 0
        # last = len(s) - 1
        # first + 9 = last
        dict1: dict[str, int] = {}
        for i in range(len(s) - 9):
            s_tmp = s[i:i+10]
            if s_tmp not in dict1:
                dict1[s_tmp] = 1
            else:
                dict1[s_tmp] += 1
        list1 = list(dict1.items())
        res = []
        for line in list1:
            if line[1] > 1:
                res.append(line[0])

        return res

res = Solution().findRepeatedDnaSequences("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT")            
print(res)