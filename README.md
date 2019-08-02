# 长安大学信息门户的模拟登录模块

本模块可以用于爬虫模拟登录长安大学信息门户

当前版本：v1.0

发行版本中含有源代码，以及打包好的一份成绩查询.exe文件，[点此处获取](https://github.com/HaneChiri/chd_portal_login/releases)

## 这个版本可以做什么

- [x] 输入账号密码后，获得一个cookies，携带此cookies可以访问需要登录才能访问的界面。
- [x] 在第一次输入账号密码登录后，可以选择性地将其以json数据格式保存到文件中，自动读取，避免频繁登录导致一些问题以及便于测试。文件中的cookies失效后，需要再次输入账号密码来登录。

## 过程记录

- [学校信息门户模拟登录之密码加密](https://hanechiri.github.io/post/portal_login_encrypt/#more)
- [学校信息门户模拟登录](https://hanechiri.github.io/post/portal_login/#more)

## 构成

- `chd_portal_login`
- `__init__.py`
  - `encrypt.py` 用于处理登录密码的加密问题
  - `login.py` 使用时导入此模块即可
- `chd_score_inquiry`
  - `score_inquiry.py` 应用登录模块来将成绩保存到.xls文件的模块
- `test.py` 用于测试登录模块是否可用的代码，由贡献者`lollipopnougat`提供

## 核心API

```python
def login(login_url, headers, check_url=None, file_name=None):
    '''
    登录到CHD信息门户
    :param login_url: 登录页面的url
    :param headers: 使用的headers
    :param check_url: 用于检查的url，尝试请求此页面并核对是否能请求到
    :param file_name: 保存cookies的文件的路径，如果为None则不保存，用于读取和保存cookies，保存的cookies为json格式
    :return: 已登录的cookies
    '''
```
## 第三方依赖

以下是使用模拟登录模块所需的模块，在命令行使用`pip install 模块名`安装即可。

- `pycryptodomex` :用于加密
- `bs4` :即`beautifulsoup4 `，用于解析网页
- `lxml`: 用于和`bs4`配合解析网页
- `requests`: 用于发起Http请求
- `xlwt`: 在成绩查询模块中使用，模拟登录模块不需要。用于将数据写入excel表格

## 示例代码

### 示例1 

```python
from chd_portal_login.login import *
if __name__ == '__main__':
    login_url = 'http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F'
    home_page_url = 'http://portal.chd.edu.cn/index.portal?.pn=p167'
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    cookies = login(login_url,headers,home_page_url)#此函数最终返回一个cookies
    #如果使用file_name参数，则可以以json形式保存与读取cookies
    #cookies=login(login_url, headers, home_page_url, file_name='cookies')
```

#### 示例1 运行结果

```bash
输入用户名: xxxxxxxxx
输入密码: xxxxxxxxx
登录成功
```

### 示例2

就是这个项目所附带的的 `test.py` ，包含了获取信息门户的成绩功能，具体请查看[代码](https://github.com/lollipopnougat/CHD_portal_login/blob/master/test.py)


#### 示例2 运行结果

![结果1](https://lollipopnougat.github.io/website-calculator/img/chdgpa1.png)
![结果2](https://lollipopnougat.github.io/website-calculator/img/chdgpa2.png)

## 登录过程分析

1. 浏览器获取登录表单数据，向`http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F`发起POST请求，得到302（重定向）的response，让浏览器请求其Location指示的网址。response给了浏览器几个cookies：CASPRIVACY、CASTGC和iPlanetDirectoryPro

2. 浏览器携带这些cookies，向新的网址`http://portal.chd.edu.cn/?ticket=ST-854426-Aye0eVjF4JmBvQyJa0le1563260380765-JRua-cas`发起GET请求，得到302的response，得到新的cookies：MOD_AUTH_CAS

3. 浏览器携带这些cookies，向新的网址`http://portal.chd.edu.cn/`发起GET请求，得到200的response，并给予新的cookies，也就是最重要的cookies：JSESSIONID

## 参考链接

- [使用cookies做PHP用户登录详解-CSDN](https://blog.csdn.net/awhip9/article/details/78007600)
- 如果导入本模块出了问题可以看这个：[Python 3.x可能是史上最详解的【导入（import）】-CSDN](https://blog.csdn.net/weixin_38256474/article/details/81228492)

