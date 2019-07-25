'''
encrypt.py
用于长安大学信息门户登录时的密码加密
'''

import requests
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad  #用于对齐
import base64
import random
import re


def random_string(length):
    '''
    获取随机字符串
    :param length:随机字符串长度
    '''
    ret_string = ''
    aes_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    for i in range(length):
        ret_string += random.choice(aes_chars)
    return ret_string


def get_aes_string(data, key, iv):
    '''
    用AES-CBC方式加密字符串
    :param data: 需要加密的字符串
    :param key: 密钥
    :param iv: 偏移量
    :return: base64格式的加密字符串
    '''
    #预处理字符串
    data = str.encode(data)
    data = pad(data, AES.block_size)  #将明文对齐

    #预处理密钥和偏移量
    key = str.encode(key)
    iv = str.encode(iv)

    cipher = AES.new(key, AES.MODE_CBC, iv)  #初始化加密器
    cipher_text = cipher.encrypt(data)  #加密

    #返回的是base64格式的密文
    cipher_b64 = str(base64.b64encode(cipher_text), encoding='utf-8')
    return cipher_b64


def encrypt_aes(data, key=None):
    '''
    进行AES加密
    :param data: 需要加密的字符串
    :param key: 密钥
    :return: 如果key存在，则返回密文，否则返回明文
    '''
    if (not key):
        return data
    else:
        data = random_string(64) + data
        iv = random_string(16)  #偏移量
        encrypted = get_aes_string(data, key, iv)
        return encrypted


def get_encrypt_salt(login_url):
    '''
    获取密钥
    :param login_url:登录页面的url
    :return: (密钥,密钥对应的cookies)
    '''
    response = requests.get(login_url)
    pattern = re.compile('var\s*?pwdDefaultEncryptSalt\s*?=\s*?"(.*?)"')
    pwdDefaultEncryptSalt = pattern.findall(response.text)[0]
    return (pwdDefaultEncryptSalt, response.cookies)


def encrypt_password(password, login_url):
    '''
    加密密码
    :param password: 需要加密的密码
    :param login_url:登录页面的url
    :return: (加密后的密码,对应的cookies)
    '''
    key, cookies = get_encrypt_salt(login_url)
    password.strip()  #去除头尾空格
    encrypted = encrypt_aes(password, key)
    return (encrypted, cookies)


if __name__ == '__main__':
    login_url = 'http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F'

    password = input('输入密码:')
    password, cookies = encrypt_password(password, login_url)
    print('加密后的密码:', password)
