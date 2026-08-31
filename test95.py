from typing import List
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        def my_fun(i, j):
                    nonlocal grid

                    #满足条件
                    if not ( 0 <= i < len(grid) and 
                            0 <= j < len(grid[i])):
                        return 

                    if grid[i][j] == '0':
                        return           

                    #如果X则.
                    if grid[i][j] == '1':
                        grid[i][j] = '0'  

                    my_fun(i-1, j)            
                    my_fun(i+1, j)            
                    my_fun(i, j-1)            
                    my_fun(i, j+1)   

        count = 0
        # already : set[tuple[int, int]] = set()
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == '1':
                    my_fun(i, j)
                    count += 1

                          

        return count    
    
res = Solution().numIslands([
["1","1","1"],
["0","1","0"],
["1","1","1"]   
])    
print(res)