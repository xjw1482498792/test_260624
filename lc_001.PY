class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        int_max = 0
        int_left = 0
        char_index_map = {}
        #快慢指针，遍历快指针      
        for index, char in enumerate(s):
            if not char in char_index_map:
                char_index_map[char] = index
                int_max = max(int_max, index - int_left +1)
            else:
                #移动慢指针
                while s[int_left] != char:      
                    del char_index_map[s[int_left]]
                    int_left += 1
                int_left += 1


        return int_max 
    
if __name__ == "__main__":
    solution = Solution()
    print(solution.lengthOfLongestSubstring("abcabcbb"))  # Output: 3
    print(solution.lengthOfLongestSubstring("bbbbb"))     # Output: 1
    print(solution.lengthOfLongestSubstring("pwwkew"))    # Output: 3    
    print(solution.lengthOfLongestSubstring(" "))   