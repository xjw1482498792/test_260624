from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # 2: 1,0
        # 2: 1,0 0,1
        # 4: 1,2 2,3 3,1
        # 5: 1,2 2,3 3,4
        def my_func(source):
            if tuple(source) in set_is_ok:
                return True

            if source[1] in set_already:
                return False                
            else:
                set_already.add(source[1])
            for tmp in prerequisites:
                if tmp[0] == source[1]:
                    res = my_func(tmp)
                    if not res:
                        return False
            set_already.remove(source[1])   

            set_is_ok.add(tuple(source))
            return True    

        set_is_ok   = set()        
        set_already = set()
        for tmp in prerequisites:
            set_already.clear()
            set_already.add(tmp[0])
            res = my_func(tmp)
            if not res:
                return False
        return True

res = Solution().canFinish(2, 
                           [[1,0],
                            [0,3],
                            [0,2],
                            [3,2],
                            [2,5],
                            [4,5],
                            [5,6],
                            [2,4]])   
print(res)     

    
