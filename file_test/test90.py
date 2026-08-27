##写文件
from datetime import datetime 
print(type(open))
with open(file='test_output.txt', mode='a', encoding='utf-8') as file:
    file.writelines(datetime.now().strftime('%Y%m%d%H%M%S\n'))
#file的路径依赖于终端执行路径
# file = open(file='test_output.txt', mode='a', encoding='utf-8')
import time
print(time.perf_counter())
#路径相关（终端路径，文件路径）
from pathlib import Path
import sys
print(Path.cwd())
print(Path(__file__))
for path in sys.path:
    print(path)
print(len(sys.path))    
#总结
'''
终端目录和文件目录
from关键字
在python命令中，从文件目录获取
在python -m 命令中，从终端目录取
'''
 