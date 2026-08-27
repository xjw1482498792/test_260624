#温习一下昨天的内容
#首先刷题
from typing import Optional
class TreeNode:
    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right
print(f'type---------------{type(Optional)}')
# age: Optional[int] = None
# age: int = None

age: int|None = None
print(f'type age is{type(age)}')
age = 18
print(f'type age is{type(age)}')
print(f'age={age}')


a = 'a'
print(id(a))
a = 'b'
print(id(a))
class Solution:
    def isSymmetric(self, root: TreeNode | None = None) -> bool:
    # def isSymmetric(self, root: TreeNode = None) -> bool:
    # def isSymmetric(self, root: TreeNode | None) -> bool:
    # def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        pass