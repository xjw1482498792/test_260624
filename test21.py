import streamlit as st
from pathlib import Path
import os
from dotenv import load_dotenv
import streamlit_authenticator as auth

#定位配置文件
ROOT = Path(__file__).absolute().parent
load_dotenv(ROOT / '.env')

#读取配置
APP_PASSWORD = os.getenv('APP_PASSWORD')

#用户列表
users = {"usernames": {
            "user20001": {
                "name": "张三",
                "password": "123456"
            }
}}

def get_auth()->auth.Authenticate:

    return auth.Authenticate(
                        users,
                        "my_app_cookie",
                        "some_signature_key",
                        cookie_expiry_days=7,
                        )


def main():
    get_auth().login(location="main")
    authentication_status = st.session_state.get("authentication_status")
    if authentication_status:
        st.success("登陆成功")
    elif authentication_status == False:
        st.error("密码错误，请重试")
    else:       
        st.warning("请输入密码") 

    name = st.session_state.get("name")
    username = st.session_state.get("username")
    print(authentication_status)
    # if not st.session_state.get("authed"):
    # if authentication_status:
    #     st.title("🔒 SAP 智能查询助手")
    #     st.caption("输入密码继续：")
    #     st.text_input( label="访问密码", type="password", key="password")
    #     if st.button("进入", type="primary"):    
    #         if st.session_state.password == APP_PASSWORD:
    #             st.session_state.authed = True
    #             st.rerun()
    #         else:
    #             st.error("密码错误请重试")
    # else:            
    #     st.title("📊 SAP 智能查询助手")


if __name__ == "__main__":
    main()    