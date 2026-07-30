# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import List, Optional

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
             return []

        slow_list = [root]
        res = []
        
        while True:
            if slow_list:
                fast_list = []
                tmp = []
                for slow in slow_list:
                    tmp.append(slow.val)
                    if slow.left:
                        fast_list.append(slow.left)
                    if slow.right:
                        fast_list.append(slow.right) 
                res.append(tmp)        
            else:
                return res

            if fast_list:
                slow_list = []
                tmp = []
                for fast in fast_list:
                    tmp.append(fast.val)               
                    if fast.left:
                        slow_list.append(fast.left)
                    if fast.right:
                        slow_list.append(fast.right)
                res.append(tmp)           

            else:
                            return res                        
        

node1 = TreeNode(3,
                 TreeNode(9, None, None),
                 TreeNode(20,
                          TreeNode(15, None, None),
                          TreeNode(7, None, None)))

print(Solution().levelOrder(node1)                    )