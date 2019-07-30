import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

def get_xsrf():
    response = requests
def zhihu_login(account,password):
    if re.match("1\d{10}",account):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf":"",
            "phone_num":account,
            "password":password
        }