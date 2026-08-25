#列表原地奇偶排序（奇数左边，偶数右边）
def sort_list(nums)->list:
    left = 0
    right = len(nums) - 1
    while left < right:
        if nums[left] % 2 == 1:
            left += 1
            continue
        if nums[right] % 2 == 0:
            right -= 1
            continue
        #left不是奇数，right不是偶数
        nums[left], nums[right] = nums[right], nums[left]    
        left += 1
        right -= 1

    return nums    

print(sort_list([1,2,3,4,5,6,7]))