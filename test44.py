# Definition for a binary tree node.
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:

    res: list = []

    def my_func(self, node: Optional[TreeNode]):


        if node:
            self.res.append(node.val)
            if node.left:
                self.my_func(node.left)
            if node.right:
                self.my_func(node.right)         

    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        self.res = []
        self.my_func(root)
        return self.res

node1 = TreeNode(1, 
                 TreeNode(2,
                             TreeNode(4, None, None),
                             TreeNode(5, 
                                      TreeNode(6, None, None),
                                      TreeNode(7, None, None))),
                 TreeNode(3, 
                          None,
                          TreeNode(8, 
                                   TreeNode(9, None, None), 
                                   None))                     )    

print(Solution().preorderTraversal(node1))
