from typing import Counter, List


# class Solution:
#     def findAnagrams(self, s: str, p: str) -> List[int]:
#         list_res = []
#         length = len(p)
#         count_p = Counter(p)
#         count_s = Counter()
#         for i, value in enumerate(s):
#             #制作滑块
#             count_s[value] += 1

#             #长度不足
#             if sum(count_s.values()) < length:
#                 continue

#             #长度过长
#             if sum(count_s.values()) > length:
#                 count_s[s[i - length]] -= 1
#                 if count_s[s[i - length]] == 0:
#                     del count_s[s[i - length]]


#             #比较结果
#             if count_p == count_s:
#                 list_res.append(i - length + 1)

#         return list_res


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        s_len, p_len = len(s), len(p)
        
        if s_len < p_len:
            return []

        ans = []
        s_count = [0] * 26
        p_count = [0] * 26
        for i in range(p_len):
            s_count[ord(s[i]) - 97] += 1
            p_count[ord(p[i]) - 97] += 1

        if s_count == p_count:
            ans.append(0)

        for i in range(s_len - p_len):
            s_count[ord(s[i]) - 97] -= 1
            s_count[ord(s[i + p_len]) - 97] += 1
            
            if s_count == p_count:
                ans.append(i + 1)

        return ans


res = Solution().findAnagrams("cbaebabacd", "abc") 
print(res)           
                