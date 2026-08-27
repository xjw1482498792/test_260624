from typing import Optional, Callable

names: list[str]
names: Optional[list]

print(type(list))
print(type(Optional))

fun = lambda x, y : x+y
operation : Callable[[int, int],str] = fun
print(operation(1,2))
print(type(operation))


class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
