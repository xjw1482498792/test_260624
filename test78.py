# class Solution:
#     def longestPalindrome(self, s: str) -> str:
#         res = ""
#         max_count = 0     
#         for i in range(len(s)):
#             if i == 0:
#                 max_count = 1
#                 res = s[0]
#                 continue
#             if i == 1 and s[0] == s[i]:
#                 max_count = 2
#                 res = s[0:2]
#                 continue

#             if i > 1:
#                 tmp_index = 0
#                 tmp_i = i
#                 origin = 0
#                 flag = 0
#                 while tmp_index < tmp_i:
#                     if s[tmp_index] == s[i] and flag != origin:
#                         flag = tmp_index

#                     if s[tmp_index] == s[tmp_i]:
#                         tmp_i     -= 1
#                         tmp_index += 1
#                     else:
#                         tmp_i = i
#                         if flag == 0:
#                             tmp_index += 1
#                         else:                            
#                             tmp_index = flag + 1
#                         origin = tmp_index
#                 length = i - origin + 1
#                 if length > max_count:
#                     res = s[origin:i + 1]
#                     max_count = length
                    
#         return res

class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n < 2:
            return s
        
        max_len = 1
        begin = 0
        # dp[i][j] 表示 s[i..j] 是否是回文串
        dp = [[False] * n for _ in range(n)]
        for i in range(n):
            dp[i][i] = True
        
        # 递推开始
        # 先枚举子串长度
        for L in range(2, n + 1):
            # 枚举左边界，左边界的上限设置可以宽松一些
            for i in range(n):
                # 由 L 和 i 可以确定右边界，即 j - i + 1 = L 得
                j = L + i - 1
                # 如果右边界越界，就可以退出当前循环
                if j >= n:
                    break
                    
                if s[i] != s[j]:
                    dp[i][j] = False 
                else:
                    if j - i < 3:
                        dp[i][j] = True
                    else:
                        dp[i][j] = dp[i + 1][j - 1]
                
                # 只要 dp[i][L] == true 成立，就表示子串 s[i..L] 是回文，此时记录回文长度和起始位置
                if dp[i][j] and j - i + 1 > max_len:
                    max_len = j - i + 1
                    begin = i
        return s[begin:begin + max_len]



res = Solution().longestPalindrome("abbcccba")   
print(res)         
                    


