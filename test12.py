# class Solution:
#     def addBinary( a: str, b: str) -> str:
# #二进制求和
# #    1111
# # +  1111
# # = 11110        
#         tmp = 0
#         max_len = max(len(a), len(b))
#         res = []
#         for i in range(max_len):
#             cur_num = 0
#             if i < (la := len(a)):
#                 cur_num += int(a[la - i - 1])
#             if i < (lb := len(b)):
#                 cur_num += int(b[lb - i - 1])
#             cur_num += tmp    
#             match cur_num:
#                 case 0:
#                     res.append('0')
#                     tmp = 0
#                 case 1:
#                     res.append('1')
#                     tmp = 0
#                 case 2:
#                     res.append('0')
#                     tmp = 1
#                 case 3:
#                     res.append('1')
#                     tmp = 1    
#         return ''.join(res[::-1]) if tmp == 0 else '1' + ''.join(res[::-1])

# #官方题解
# class Solution:
#     def addBinary(self, a, b) -> str:
#         return '{:b}'.format(int(a, 2) + int(b, 2))


# print(Solution.addBinary('1111', '1111'))


#测试一下，正数第1个元素
#测试一下，正数第2个元素
#测试一下，倒数第2个元素
#测试一下，倒数第1个元素
#测试一下，正数第2个元素 到 倒数第2个元素 的所有元素
#  a  b  c  d
#  0  1  2  3
# -4 -3 -2 -1
# a = 'abcd'
# print(a[0])
# print(a[1])
# print(a[-2])
# print(a[-1])
# print(a[1:-1])
# print(a[1:2])


# a = 'abcd'
# print(a[::-1])
# print(a[::1])

#练习二进制输出
# def addBinary(a: str, b: str)-> str:
#     return f'{int(a,2) + int(b,2):b}'

def addBinary(a: str, b: str)-> str:
    return'{:b}'.format(int(a,2) + int(b,2))

print(addBinary('1111', '1111'))