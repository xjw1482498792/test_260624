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
        res = True
#层序遍历
        que1 = Queue()
        que2 = Queue()
        list_val = []
        que1.put(root)
        while not (que1.empty() and que2.empty()):
            while not que1.empty():
                tmp = que1.get()
                list_val.append(tmp.val)
                if tmp.left:
                    que2.put(tmp.left)
                if tmp.right:
                    que2.put(tmp.right)

            if list_val:                    
                print(list_val)
                #做轴对称判断
                tmp_list = list_val[::-1]
                print(list_val == tmp_list)
                if not list_val == tmp_list:
                    return False
                list_val.clear()   

            while not que2.empty():
                tmp = que2.get()
                list_val.append(tmp.val)
                if tmp.left:
                    que1.put(tmp.left)
                if tmp.right:
                    que1.put(tmp.right)  

            if list_val:                    
                print(list_val)
                tmp_list = list_val[::-1]
                print(list_val == tmp_list)   
                if not list_val == tmp_list:
                        return False                             
                list_val.clear() 

        return True                                            

# #我先深度遍历打印一下
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

root = TreeNode(1, 
                TreeNode(2, 
                         None,
                         TreeNode(3)                         ),
                TreeNode(2,
                         None,
                         TreeNode(3)))

print(f'res====={Solution().isSymmetric(root)}')