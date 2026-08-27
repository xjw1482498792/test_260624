import sys
a = 'moduleA'
for path in sys.path:
    print(path)
print(len(sys.path))    
# from yanshi_python import mb
# from . import mb
import mb
print(mb.b)
'''
python命令：    python    yanshi_python/ma.py
sys.path中的项目路径是文件路径，git0625/yanshi_python

python -m命令： python -m yanshi_python.ma
sys.path中的项目路径是终端路径，git0625
'''