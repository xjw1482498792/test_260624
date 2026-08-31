from typing import List
class Solution:
    def countBattleships(self, board: List[List[str]]) -> int:
        count = 0
        already : set[tuple[int, int]] = {}
        def my_fun(i, j):
            #满足条件
            if not ( 0 <= i < len(board) and 
                     0 <= j < len(board[i])):
                return 
            
            #遍历过直接返回true
            if (i, j) in already:
                 return        
                 
            #遍历过的记录
            already.add((i, j))

            #如果X则.
            if board[i][j] == 'X':
                board[i][j] == '.'                       

            #如果上下左右都没有X，那么计数加1
            if not (
                        ( 
                            0 <= i - 1 < len(board) and  
                            0 <= j < len(board[i])  and 
                            board[i][j] == 'X' 
                        )   #上节点有值 
                        or 
                        ( 
                            0 <= i + 1 < len(board) and
                            0 <= j < len(board[i])  and
                            board[i][j] == 'X'
                        )    #下节点有值
                        or
                        (
                            0 <= i < len(board) and 
                            0 <= j - 1 < len(board[i]) and 
                            board[i][j] == 'X'
                        )
                        or
                        (
                            0 <= i < len(board) and
                            0 <= j + 1 < len(board[i]) and
                            board[i][j] == 'X'        
                        )
                ):             
                    count += 1
            #上下左右只决定遍历方向              
            my_fun(i-1, j)            
            my_fun(i+1, j)            
            my_fun(i, j-1)            
            my_fun(i, j+1)   
            
        my_fun(0, 0)
        return count    