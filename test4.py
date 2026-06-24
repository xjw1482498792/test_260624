class Solution:
    def romanToInt(self, s: str) -> int:
       dict1 = { "I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000 }
       add = 0
       reduce = 0
       for index, war in enumerate(s):
           if index == len(s) - 1:                
                add += dict1[war]
           elif dict1[war] < dict1[s[index + 1]]:
               reduce += dict1[war]
           else:
               add += dict1[war]
       return add - reduce
    
if __name__ == "__main__":
    solution = Solution()
    print(solution.romanToInt("III"))     # Output: 3
    print(solution.romanToInt("IV"))      # Output: 4
    print(solution.romanToInt("IX"))      # Output: 9
    print(solution.romanToInt("LVIII"))   # Output: 58
    print(solution.romanToInt("MCMXCIV")) # Output: 1994    