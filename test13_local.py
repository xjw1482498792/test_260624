
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        if l1 is None:
            return l2
        elif l2 is None:
            return l1
        elif l1.val < l2.val:
            l1.next = self.mergeTwoLists(l1.next, l2)
            return l1
        else:
            l2.next = self.mergeTwoLists(l1, l2.next)
            return l2

# def to_list(arr):
#     dummy = ListNode(0)
#     cur = dummy
#     for v in arr:
#         cur.next = ListNode(v)
#         cur = cur.next
#     return dummy.next

# def print_list(node):
#     vals = []
#     while node:
#         vals.append(node.val)
#         node = node.next
#     print(vals)
list1 = ListNode(1,ListNode(2,ListNode(4)))
list2 = ListNode(1,ListNode(3,ListNode(4)))
res = Solution().mergeTwoLists(list1, list2)
while res:
    print(res.val, end=" -> ")
    res = res.next