from typing import List
class Solution:
    def countBattleships(self, board: List[List[str]]) -> int:
        def my_fun(i, j):
            if not(0 <= i < len(board) and 0 <= j < len(board[i])):
                return
            if board[i][j] == '.':
                return
            board[i][j] = '.'
            my_fun(i - 1, j)
            my_fun(i + 1, j)
            my_fun(i, j - 1)
            my_fun(i, j + 1)

        count = 0
        for i  in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 'X':
                    count += 1
                    my_fun(i, j)
        return count                 


res = Solution().countBattleships([
["X",".",".","X"],
[".",".",".","X"],
[".",".",".","X"]
])            
print(res)