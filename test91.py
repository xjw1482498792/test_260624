#二叉树最小深度
from typing import Optional
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left


        self.right = right
# class Solution:
#     def minDepth(self, root: Optional[TreeNode]) -> int:
#         if not root:
#             return 0
        
#         min_length = float('inf')
#         cur_length = 0
#         def get_min(node: Optional[TreeNode])->None:
#             nonlocal min_length, cur_length
#             # if node is None:
#             #     return
#             cur_length += 1
#             if node.left is None and node.right is None:
#                 min_length = min(min_length, cur_length)
#             else:                                                
#                 get_min(node.left)
#                 get_min(node.right)
#             cur_length -= 1
#         get_min(root)    
#         return min_length
# 
class Solution:
    def minDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        
        if not root.left and not root.right:
            return 1
        
        min_depth = 10**9
        if root.left:
            min_depth = min(self.minDepth(root.left), min_depth)
        if root.right:
            min_depth = min(self.minDepth(root.right), min_depth)
        
        return min_depth + 1
     

root = TreeNode(3,
                TreeNode(9),
                TreeNode(20,
                         TreeNode(15),
                         TreeNode(7)))

res = Solution().minDepth(root)
print(res)