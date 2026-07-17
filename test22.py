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
            #梳理下标准streamlit登录流程，然后过
            #用户信息存在数据库
            #该处只处理登录状态（未登录（密码错误，密码正确），已登陆）
            st.stop()
            get_auth().login(location="main")    
            # st.rerun()
            #到这里有2种状态， 密码错误，密码正确，已登陆
            state = st.session_state.get("authentication_status")
            if state == False:    
                st.error("密码错误，请重试")
                return

            if state == None:
                return
            st.title("新页面")        




if __name__ == "__main__":
    main()    