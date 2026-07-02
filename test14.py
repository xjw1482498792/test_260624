class Solution:
    def isPalindrome(self, s: str) -> bool:
        '''
        只保留字母，且大写转小写，验证回文串
        '''
        set1 = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        res = ''
        for tmp in s:
            if tmp in set1:
                res += tmp.lower() 
        return True if res == res[::-1] else False
    
print(Solution().isPalindrome("0P"))