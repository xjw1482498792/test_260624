class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        strs1 = ""
        index = 0
        if len(strs) == 1:
            return strs[0]
        while True:
            for idx, tmp in enumerate(strs):
                # 如果当前字符串的长度不够，或者当前字符不相同，则返回结果
                if ((index >= len(tmp) or index >= len(strs[idx + 1]))                    
                or tmp[index] != strs[idx + 1][index]):
                    return strs1
                # 只有当所有字符串都相同才会执行到这里
                if idx == len(strs) - 2:
                    strs1 += tmp[index]
                    break
            index += 1        

if __name__ == "__main__":
    s = Solution()
    print(s.longestCommonPrefix(["a"]))