from typing import Optional, Callable

names: list[str]
names: Optional[list]

print(type(list))
print(type(Optional))

fun = lambda x, y : x+y
operation : Callable[[int, int],str] = fun
print(operation(1,2))
print(type(operation))

#题目，根节点到叶子节点的和=目标值
class TreeNode:
    def __init__(self, val=0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right
# class Solution:
#     def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
#         sum = 0
         
# #1
# #22
# #3333
#         def my_path(node: Optional[TreeNode]):
#             nonlocal sum
#             if node is None:
#                 return False
#             sum += node.val

#             if node.left is None and node.right is None:
#                  #叶子节点and等于目标值
#                  if sum == targetSum:
#                      sum -= node.val 
#                      return True

#             res_left  = my_path(node.left)
#             res_right = my_path(node.right) 

#             sum -= node.val      

#             return res_left or res_right     
#         return my_path(root)

import collections
class Solution:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        if not root:
            return False
        que_node = collections.deque([root])
        que_val = collections.deque([root.val])
        while que_node:
            now = que_node.popleft()
            temp = que_val.popleft()
            if not now.left and not now.right:
                if temp == sum:
                    return True
                continue
            if now.left:
                que_node.append(now.left)
                que_val.append(now.left.val + temp)
            if now.right:
                que_node.append(now.right)
                que_val.append(now.right.val + temp)
        return False
    
root = TreeNode(5,
                TreeNode(4,
                         TreeNode(11,
                                  TreeNode(7),
                                  TreeNode(2)),
                         None),
                TreeNode(8,
                         TreeNode(13),
                         TreeNode(4,
                                  None,
                                  TreeNode(1)),                         ))

res = Solution().hasPathSum(root,22)    
print(res)

