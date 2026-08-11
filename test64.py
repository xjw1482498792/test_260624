# class Solution:
#     def checkInclusion(self, s1: str, s2: str) -> bool:
#         #需要两个集合
#         #所有s1的元素set1，和set1弹出的set2
#         #滑动
#         dict1: dict[str: int] = {}
        
#         for war in s1:
#             if war not in dict1:
#                 dict1[war] = 1
#             else:
#                 dict1[war] += 1

#         dict2 = dict1.copy()
#         for war2 in s2:

#             if war2 in dict2:
#                 dict2[war2] -= 1
#                 if dict2[war2] == 0:
#                     del dict2[war2]
#                     if not dict2:
#                         return True
#             else:
#                 dict2 = dict1.copy()        
#         return False


# class Solution:
#     def checkInclusion(self, s1: str, s2: str) -> bool:
#         #需要两个集合
#         #所有s1的元素set1，和set1弹出的set2
#         #滑动
#         dict1 = {}
#         for war in s1:
#             if war not in dict1:
#                 dict1[war] = 1
#             else:
#                 dict1[war] += 1      

#         for i in range(len(s2) - len(s1) + 1):
#             res = self.is_ok( dict1, s2[i: i + len(s1)])
#             if res:
#                 return True
#         return False    

#     def is_ok(self, dict1: dict, s2: str):
#         dict2 = dict1.copy()
#         for war2 in s2:
#             if war2 in dict2:
#                 dict2[war2] -= 1
#                 if dict2[war2] == 0:
#                     del dict2[war2]
#             else:
#                 return False
#         return True      


from typing import Counter


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        m = len(s1)
        if m > len(s2):
            return False

        cnt_s1 = Counter(s1)  # 统计 s1 的每种字母的出现次数
        cnt_t = Counter()  # 对于 s2 的长为 m 的子串 t，统计 t 的每种字母的出现次数
        for i, c in enumerate(s2):
            # 1. 进入窗口
            cnt_t[c] += 1
            if i < m - 1:  # 窗口大小不足 m
                continue
            # 2. 判断子串 t 的每种字母的出现次数是否均与 s1 的相同
            if cnt_t == cnt_s1:
                return True
            # 3. 离开窗口，为下一个循环做准备
            cnt_t[s2[i - m + 1]] -= 1
        return False


                    
res = Solution().checkInclusion("adc", "dcda" )    
print(res)
            # set1.remove()

