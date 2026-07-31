from pathlib import Path

path = Path(__file__).absolute().parent / 'test_package' / 'test1'

#父级路径缺失不报错&目标路径存在不报错
path.mkdir( parents=True, exist_ok=True )
print(path)