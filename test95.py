from typing import List
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        count = 0
        already : set[tuple[int, int]] = set()
        def my_fun(i, j):
            nonlocal count, grid

            #满足条件
            if not ( 0 <= i < len(grid) and 
                     0 <= j < len(grid[i])):
                return True
            
            #遍历过直接返回true
            if (i, j) in already:
                return True   
            #遍历过的记录
            if (i, j) not in already:            
                already.add((i, j))  

            if grid[i][j] == 0:
                return True                          

            #没遍历过，并且是0
            if ((i, j) not in already and 
                grid[i][j] == '0'):
                return True                

            my_fun(i-1, j)            
            my_fun(i+1, j)            
            my_fun(i, j-1)            
            my_fun(i, j+1)   

            #如果X则.
            if grid[i][j] == '1':
                grid[i][j] = '0'                        

            #如果上下左右都没有X，那么计数加1                
            if not (
                        ( 
                            0 <= i - 1 < len(grid) and  
                            0 <= j < len(grid[i])  and 
                            grid[i - 1][j] == '1' 
                        )   #上节点有值 
                        or 
                        ( 
                            0 <= i + 1 < len(grid) and
                            0 <= j < len(grid[i])  and
                            grid[i + 1][j] == '1'
                        )    #下节点有值
                        or
                        (
                            0 <= i < len(grid) and 
                            0 <= j - 1 < len(grid[i]) and 
                            grid[i][j - 1] == '1'
                        )   #左节点有值
                        or
                        (
                            0 <= i < len(grid) and
                            0 <= j + 1 < len(grid[i]) and
                            grid[i][j + 1] == '1'        
                        )   #右节点有值
                ):             
                    count += 1                      
            
        my_fun(0, 0)
        return count    
    
res = Solution().numIslands([
["1","1","1"],
["0","1","0"],
["1","1","1"]   
])    
print(res)