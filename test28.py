import streamlit as st


#加载环境变量
from dotenv import load_dotenv, dotenv_values
from pathlib import Path
import os

# print(f'__file__:{__file__}')
load_dotenv(Path(__file__).resolve().parent / ".env")
PASSWORD = os.getenv("APP_PASSWORD")
PASSWORD2 = dotenv_values(Path(__file__).resolve().parent / ".env").get("APP_PASSWORD")
# print(f"PASSWORD2:{ PASSWORD2 }")

# print(f'Path:{Path(__file__).resolve().parent / ".env"}')
# print(f'PASSWORD:{PASSWORD}')
#从环境读取pwd


#密码校验
if not st.session_state.get("authed"):

    st.title("🔒 SAP 智能查询助手")
    st.caption("演示项目 · 输入访问密码继续")
    pwd = st.text_input("访问密码", type="password", key="_pwd_input")
    if st.button("进入", type="primary"):
        if pwd == PASSWORD:
            st.session_state.authed = True
            st.rerun()
        else:
            st.error("密码错误")  
else:
    # 顶部
    st.title(f"📊 SAP 智能查询助手")
    st.caption(
        "自然语言问 SAP 业务数据 · Schema RAG + LangGraph 自修复 Agent · "
        f"DeepSeek 驱动"
    )          