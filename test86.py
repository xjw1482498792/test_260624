# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

#检查二叉树根节点是否对称       
from queue import Queue  
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def recur(L, R):
            if not L and not R: return True
            if not L or not R or L.val != R.val: return False
            return recur(L.left, R.right) and recur(L.right, R.left)

        return recur(root.left, root.right)


# class Solution:
#     def isSymmetric(self, root: Optional[TreeNode]) -> bool:
#         res = True
# #层序遍历
#         que1 = Queue()
#         que2 = Queue()
#         list_val = []
#         que1.put(root)
#         while not (que1.empty() and que2.empty()):
#             while not que1.empty():
#                 tmp = que1.get()
#                 if tmp:
#                     list_val.append(tmp.val)
#                     que2.put(tmp.left)   
#                     que2.put(tmp.right)                      
#                 else:
#                     list_val.append(None)    
#                     # if tmp.left:
#                     #     que2.put(tmp.left)
#                     # if tmp.right:
#                     #     que2.put(tmp.right)
                      

#             if list_val:                    
#                 print(list_val)
#                 #做轴对称判断
#                 tmp_list = list_val[::-1]
#                 print(list_val == tmp_list)
#                 if not list_val == tmp_list:
#                     return False
#                 list_val.clear()   

#             while not que2.empty():
#                 tmp = que2.get()
#                 if tmp:
#                     list_val.append(tmp.val)
#                     que1.put(tmp.left)   
#                     que1.put(tmp.right) 
#                 else:
#                     list_val.append(None)                        
#                     # if tmp.left:
#                     #     que1.put(tmp.left)
#                     # if tmp.right:
#                     #     que1.put(tmp.right)  
                                      

#             if list_val:                    
#                 print(list_val)
#                 tmp_list = list_val[::-1]
#                 print(list_val == tmp_list)   
#                 if not list_val == tmp_list:
#                         return False                             
#                 list_val.clear() 

#         return True                                            

# #我先层序遍历打印一下
        # que.put(root)
        # while not que.empty():
        #     tmp = que.get()
        #     print(tmp.val)
        #     if tmp.left:
        #         que.put(tmp.left)
        #     if tmp.right:    
        #         que.put(tmp.right)

# #我先深度遍历打印一下
#         if root:
#             print(root.val)
#         else:
#             return    
#         self.isSymmetric(root.left)
#         self.isSymmetric(root.right)
# 1
# 2 2
# 4 3 3 4
# 5 6 7 8 8 7 6 5
# a b c d e f g h h g f e d c b a

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
                                           TreeNode('h')))                         ),
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

print(f'res====={Solution().isSymmetric(root)}')
