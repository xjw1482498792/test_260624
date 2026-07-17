class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        # 1

        # 1 1
        
        # 1 2 1
        # 左边1  1+1=2  右边1  

        #1 3 3 1
        # 左边1  1+3=4  3+1=4 右边1

        #1 4 6 4 1
        # 左边1  1+3=4  3+3=6  3+1=4 右边1

        if numRows == 1:
            return [[1]]
        if numRows == 2:
            return [[1], [1, 1]]
        
        res = [[1], [1, 1]]
        for index in range(2, numRows):
            last = res[index - 1]
            new = [1]
            middle = [last[index2] + last[index2 + 1] for index2 in range(len(last) - 1)]
            new.extend(middle)
            new.append(1)
            res.append(new)
        return res        

print(Solution().generate(3))