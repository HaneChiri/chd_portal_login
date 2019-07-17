'''
测试模块
用于测试是否可登录
'''

from portal_login.login import *
if __name__ == '__main__':
    login_url='http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F'
    home_page_url='http://portal.chd.edu.cn/index.portal?.pn=p167'
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    cookies=login(login_url,headers,home_page_url)#此函数最终返回一个cookies
    print(cookies)