from datetime import datetime
import time
import streamlit as st
from functools import cache

# list set dict tuple int float bool 
# 模块 类 方法和变量
@st.cache_resource(show_spinner="加载中")
def fun1()->str:
    # now = time.strptime()
    # print(datetime.now().strftime("%Y-%m-%d "))
    now = time.strftime("%Y年%m月%d日")
    print(f'fun1打印当前日期：{ now }')
    return f'fun1返回值为：{ now }'

@cache
def fun2()->str:
    now = time.strftime("%H:%M:%S")
    print(f'fun2打印当前时间：{ now }')
    return f'fun2返回值为：{ now }'

# print(fun1())
# print(fun1())
# print(fun2())
# print(fun2())


