'''
登录长安大学信息门户
'''


# 以下是确保此模块本身运行时也能够正确导入自定义模块的语句，请勿移动顺序
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取绝对路径
sys.path.append(BASE_DIR + '\\..')


import json
import requests
from bs4 import BeautifulSoup
import logging
from portal_login.encrypt import *



def get_login_data(login_url, headers):
    '''
    长安大学登录表单数据解析
    :param login_url: 登录页面的url
    :return (登录信息字典,获取时得到的cookies)
    '''
    username = input('输入用户名: ')
    password = input('输入密码: ')
    username.strip()
    password.strip()  # 去除头尾空格

    # 获取登录所需表单数据
    response = requests.get(login_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    # 获取密钥来加密密码
    pattern = re.compile('var\s*?pwdDefaultEncryptSalt\s*?=\s*?"(.*?)"')
    key = pattern.findall(html)[0]
    password = encrypt_aes(password, key)

    lt = soup.find('input', {'name': 'lt'})['value']
    dllt = soup.find('input', {'name': 'dllt'})['value']
    execution = soup.find('input', {'name': 'execution'})['value']
    _eventId = soup.find('input', {'name': '_eventId'})['value']
    rmShown = soup.find('input', {'name': 'rmShown'})['value']

    login_data = {
        'username': username,
        'password': password,
        'lt': lt,
        'dllt': dllt,
        'execution': execution,
        '_eventId': _eventId,
        'rmShown': rmShown
    }
    logging.debug('成功获取表单数据')
    return (login_data, response.cookies)


def check_cookies(check_url, cookies, headers):
    '''
    检查cookies是否成功登录
    :param check_url: 用于检查的url，如果为None，则返回None
    :return: 登录成功为True，反之为False，如果check_url为None，则返回None
    '''
    if check_url == None:
        return None
    response = requests.get(check_url, headers=headers, cookies=cookies)
    if response.url == check_url:
        return True
    else:
        return False


def join_cookies(cookies1, cookies2):
    '''
    将cookies1和cookies2合并
    '''
    cookies = dict(cookies1, **cookies2)
    cookies = requests.utils.cookiejar_from_dict(cookies)
    return cookies


def save_cookies(cookies, output='cookies'):
    '''
    保存cookies到文件
    :param cookies: 需要保存的cookies
    :param output: 输出文件的路径
    '''
    try:
        cookies = requests.utils.dict_from_cookiejar(cookies)
        with open(output, 'w') as fp:
            json.dump(cookies, fp)
        logging.info('保存cookies成功')
    except:
        logging.info('保存cookies失败')


def load_cookies(input='cookies', check_url=None):
    '''
    从文件中读取cookies
    :param input: 输入文件的路径
    :param check_url: 用于检查cookies有效性的url，如果为None，则不检查
    :return: cookies，如果读取失败，或cookies无效，返回None
    '''
    try:
        with open(input, 'r') as fp:
            cookies = json.load(fp)
        cookies = requests.utils.cookiejar_from_dict(cookies)
        check = check_cookies(check_url, headers=headers, cookies=cookies)
        if check == False:
            # 如果cookies无效，返回None
            logging.info('读取到无效的cookies')
            cookies = None
        elif check == True:
            logging.info('读取到有效的cookies')
        else:
            logging.info('读取到未检查有效性的cookies')
    except:
        cookies = None
    finally:
        return cookies


def login(login_url, headers, check_url=None, file_name=None):
    '''
    登录到CHD信息门户
    :param login_url: 登录页面的url
    :param headers: 使用的headers
    :param check_url: 用于检查的url，尝试请求此页面并核对是否能请求到
    :param file_name: 保存cookies的文件的路径，如果为None则不保存，用于读取和保存cookies
    :return: 已登录的cookies
    '''
    if file_name != None and isinstance(file_name, str):
        cookies = load_cookies(file_name, check_url)
        if cookies != None:

            return cookies

    data, cookies = get_login_data(login_url, headers)  # 获取登录数据

    response = requests.post(login_url,
                             headers=headers,
                             data=data,
                             cookies=cookies,
                             allow_redirects=False)
    while response.status_code == 302:  # 如果响应状态是“重定向”
        # 合并新获取到的cookies
        cookies = join_cookies(cookies, response.cookies)
        # 获取下一个需要跳转的url
        next_station = response.headers['Location']
        response = requests.post(next_station,
                                 headers=headers,
                                 cookies=cookies,
                                 allow_redirects=False)

    cookies = join_cookies(cookies, response.cookies)
    # 登录检查
    check = check_cookies(check_url, headers=headers, cookies=cookies)
    if check == True:
        logging.info("登录成功")
        # 如果登录成功，且指定了保存的文件，则保存cookies以备下次使用
        if file_name != None:
            save_cookies(cookies, file_name)
    elif check == False:
        logging.info("登录失败")
    else:
        pass

    return cookies


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    login_url = 'http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F'
    home_page_url = 'http://portal.chd.edu.cn/index.portal?.pn=p167'
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    login(login_url, headers, home_page_url, file_name='cookies')
