import re
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
       res = re.search( needle, haystack )
       return res.span()[0] if res else -1
       print(res.span())

res = Solution().strStr("hello", "ll")       
print(res)