
from typing import Optional
class TreeNode:
    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

#对称二叉树
# 1
# 22
# 4334
# 56788765
# abcdefghhgfedcba
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def my_symmetric( left: Optional[TreeNode], right: Optional[TreeNode])->bool:                        
            if left is None and right is None:
                return True
            if left is None or right is None:
                return False
            if left.val != right.val:
                return False
            print(left.val, right.val)                
            return ( my_symmetric(left.left, right.right) and 
                     my_symmetric(left.right, right.left) )
        return my_symmetric(root.left, root.right)
    
root = TreeNode(1,
                TreeNode(2,
                         TreeNode(4,
                                  TreeNode(5,
                                           TreeNode('a'),
                                           TreeNode('b')),
                                  TreeNode(6,
                                           TreeNode('c'),
                                           TreeNode('d'))),
                         TreeNode(3,
                                  TreeNode(7,
                                           TreeNode('e'),
                                           TreeNode('f')),
                                  TreeNode(8,
                                           TreeNode('g'),
                                           TreeNode('h')))),
                TreeNode(2,
                         TreeNode(3,
                                  TreeNode(8,
                                           TreeNode('h'),
                                           TreeNode('g')),
                                  TreeNode(7,
                                           TreeNode('f'),
                                           TreeNode('e'))),
                         TreeNode(4,
                                  TreeNode(6,
                                           TreeNode('d'),
                                           TreeNode('c')),
                                  TreeNode(5,
                                           TreeNode('b'),
                                           TreeNode('a')))))    

res = Solution().isSymmetric(root=root)
print(res)