# Definition for singly-linked list.
from typing import Optional
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
# class Solution:
#     def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
#         cur = ListNode()
#         res = cur
#         while list1 and list2:
#             if list1.val < list2.val:
#                 cur.next = ListNode(list1.val)
#                 cur = cur.next
#                 list1 = list1.next
#             else:
#                 cur.next = ListNode(list2.val)
#                 cur = cur.next  
#                 list2 = list2.next
#         if list1:
#             cur.next = list1
#             return res.next
#         else:
#             cur.next = list2
#             return res.next   
# 
# 1 2 4
# 1 3 4
# 1 1 2 3 4 4
#用递归
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # res = ListNode() if 
        if list1 is None:
            return list2
        if list2 is None:
            return list1

        if list1.val < list2.val:
            #递归比较较小的，那个节点后移一位，返回节点要一节一节增加
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2


    
par1 = ListNode(1, ListNode(2, ListNode(4, None)))   
par2 = ListNode(1, ListNode(3, ListNode(4, None)))
res = Solution().mergeTwoLists(par1, par2)
while res:
    print(res.val)
    res = res.next