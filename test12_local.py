
class Solution:
    def mergeTwoLists(self, list1: list, list2: list) -> list:
#1,3,4,5
#1,2,4,5
#11,23,44,55
        res = []
        index1 = 0
        index2 = 0
        while index1 < len(list1) and index2 < len(list2):
            if list1[index1] and list2[index2]:
                if list1[index1] < list2[index2]:
                    res.append(list1[index1])
                    index1 += 1
                else:
                    res.append(list2[index2])
                    index2 += 1
        while index1 < len(list1):
            res.append(list1[index1])
            index1 += 1
        while index2 < len(list2):
            res.append(list2[index2])
            index2 += 1
        return res

res = Solution().mergeTwoLists([1,2,4],[1,3,4])                                
print(res)