from typing import Set, List


# class Solution:
#     def exist(self, board: List[List[str]], word: str) -> bool:
#         for i in range(len(board)):
#             for j in range(len(board[i])):
#                 if board[i][j] == word[0]:
#                     already = set()
#                     #开始遍历
#                     if self.my_return(board, already, word, 0, i, j):
#                         return True
#         return False            

#     def my_return(self, 
#                   board: List[List[str]], 
#                   already: Set[tuple[int,int]],  # type: ignore
#                   word: str,
#                   layer: int,
#                   i: int, 
#                   j: int): # type: ignore
        
#         tup1 = (i, j)

#         if board[i][j] != word[layer]:
#             return False

#         if tup1 in already:
#             return False

#         if layer == len(word) - 1:
#             return True

#         already.add(tup1)
#         bool1 = bool2 = bool3 = bool4 = False
#         if 0 <= i - 1 < len(board):
#             bool1 = self.my_return(board, already, word, layer + 1, i - 1, j)  
#         if 0 <= i + 1 < len(board):
#             bool2 = self.my_return(board, already, word, layer + 1, i + 1, j)  
#         if 0 <= j - 1 < len(board[i]):
#             bool3 = self.my_return(board, already, word, layer + 1, i, j - 1)  
#         if 0 <= j + 1 < len(board[i]):
#             bool4 = self.my_return(board, already, word, layer + 1, i, j + 1)  
#         bool_last = bool1 or bool2 or bool3 or bool4
#         if not bool_last:
#             already.remove((i, j))

#         return bool_last


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def check(i: int, j: int, k: int) -> bool:
            if board[i][j] != word[k]:
                return False
            if k == len(word) - 1:
                return True
            
            visited.add((i, j))
            result = False
            for di, dj in directions:
                newi, newj = i + di, j + dj
                if 0 <= newi < len(board) and 0 <= newj < len(board[0]):
                    if (newi, newj) not in visited:
                        if check(newi, newj, k + 1):
                            result = True
                            break
            
            visited.remove((i, j))
            return result

        h, w = len(board), len(board[0])
        visited = set()
        for i in range(h):
            for j in range(w):
                if check(i, j, 0):
                    return True
        
        return False



res = Solution().exist(
[["A","B","C","E"],
 ["S","F","E","S"],
 ["A","D","E","E"]],
                 'ABCESEEEFS')            

print(res)