from typing import Optional, List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:        
        def my_fun(node: Optional[TreeNode], res: list[int])->list[int]:      
            if node:
                res.append(node.val)
            else:
                return res
            my_fun(node.left, res)    
            my_fun(node.right, res)   
            return res
        return my_fun(root, []) 

root = TreeNode(1,
                TreeNode(2,
                         TreeNode(4),
                         TreeNode(5,
                                  TreeNode(6),
                                  TreeNode(7))),
                TreeNode(3,
                         None,
                         TreeNode(8,
                                  TreeNode(9),
                                  None)))

res = Solution().preorderTraversal(root)        
print(res)
            