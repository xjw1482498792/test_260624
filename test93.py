#搞下open文件流，然后以复现项目为主
#相关涉及日期时间，路径等
from datetime import datetime

line = datetime.now().strftime('%Y-%m-%d %H%M%S') + '\n'
with open(file='output_2.txt', mode='a', encoding='utf-8') as file:
    file.writelines(line)

from pathlib import Path
#文件路径
cur = Path(__file__)
#终端路径
cwd = Path().cwd()

print(cur)
print(cwd)

#
import time
print(time.perf_counter())

#
import sys
for path in sys.path:
    print(path)
print(len(sys.path))
