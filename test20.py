class Solution:
    def climbStairs(self, n: int) -> int:
        # 1节 -> 1
        # 2节 -> 1 + 1
        #        2
        # 3节 -> 1 + 1 + 1
        #     -> 1 + 2
        #     -> 2 + 1
        #F(1) = 1
        #F(2) = 2
        #F(3) = 3
        #F(3) = F(2) + F(1) = 3
        #F(4) = F(3) + F(2) = 5
        #F(5) = F(4) + F(3) = 8
        if n == 1:
            return 1
        if n == 2:
            return 2
        
        slow = 1
        fast = 2
        for index in range(3, n + 1):
            res = slow + fast
            slow = fast
            fast = res

        return res
    
print(Solution().climbStairs(10))