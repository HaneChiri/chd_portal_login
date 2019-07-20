'''
登录长安大学信息门户
'''

#确保此模块本身运行时也能够正确导入自定义模块的语句
import sys,os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))#获取绝对路径
sys.path.append(BASE_DIR+'\\..')

from portal_login.encrypt import *
import requests

from bs4 import BeautifulSoup

def get_login_data(login_url,headers):

    '''
    长安大学登录表单数据解析
    :param login_url: 登录页面的url
    :return (登录信息字典,获取时得到的cookies)
    '''
    username=input('input username:')
    password=input('input password:')
    username.strip()
    password.strip()#去除头尾空格
    

    #获取登录所需表单数据
    response=requests.get(login_url,headers=headers)
    html=response.text
    soup=BeautifulSoup(html,'lxml')
    #获取密钥来加密密码
    pattern = re.compile('var\s*?pwdDefaultEncryptSalt\s*?=\s*?"(.*?)"')
    key = pattern.findall(html)[0]
    password=encrypt_aes(password,key)

    lt=soup.find('input',{'name':'lt'})['value']
    dllt=soup.find('input',{'name':'dllt'})['value']
    execution = soup.find('input', {'name': 'execution'})['value']
    _eventId = soup.find('input', {'name': '_eventId'})['value']
    rmShown = soup.find('input', {'name': 'rmShown'})['value']
    
    login_data={
        'username': username,
        'password': password,
        'lt': lt,
        'dllt': dllt,
        'execution': execution,
        '_eventId': _eventId,
        'rmShown': rmShown
    }

    return (login_data,response.cookies)

def join_cookies(cookies1,cookies2):
    '''
    将cookies1和cookies2合并
    '''
    cookies=dict(cookies1,**cookies2)
    cookies=requests.utils.cookiejar_from_dict(cookies)
    return cookies


def login(login_url,headers,check_url=None):
    '''
    登录到CHD信息门户
    :param login_url: 登录页面的url
    :param headers: 使用的headers
    :param check_url: 用于检查的url，尝试请求此页面并核对是否能请求到
    :return: 已登录的cookies
    '''
    data,cookies=get_login_data(login_url,headers)#获取登录数据
    
    response=requests.post(login_url,headers=headers,data=data,cookies=cookies,allow_redirects=False)    
    while response.status_code == 302:#如果响应状态是“重定向”
        #合并新获取到的cookies
        cookies=join_cookies(cookies,response.cookies)
        #获取下一个需要跳转的url
        next_station=response.headers['Location']
        response=requests.post(next_station,headers=headers,cookies=cookies,allow_redirects=False)

    cookies=join_cookies(cookies,response.cookies)
    #登录检查
    if check_url != None:
        response = requests.get(check_url,headers=headers,cookies=cookies)
        if response.url==check_url:
            print("登录成功")
        else:
            print("登录失败")
    return cookies



if __name__ == '__main__':
    login_url='http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F'
    home_page_url='http://portal.chd.edu.cn/index.portal?.pn=p167'
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    login(login_url,headers,home_page_url)