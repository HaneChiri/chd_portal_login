# 长安大学信息门户的模拟登录模块

本模块可以用于爬虫模拟登录长安大学信息门户

# 构成


- `portal_login`

  - `__init__.py`
  - `encrypt.py`
  - `login.py`

# 示例代码

```python
from portal_login.login import *
if __name__ == '__main__':
    login_url='http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F'
    home_page_url='http://portal.chd.edu.cn/index.portal?.pn=p167'
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    cookies=login(login_url,headers,home_page_url)#此函数最终返回一个cookies
```

运行结果：

```python
input username:xxxxxxxxx
input password:xxxxxxxxx
登录成功
```



# 登录过程分析
1. 浏览器获取登录表单数据，向`http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F`发起POST请求，得到302（重定向）的response，让浏览器请求其Location指示的网址。response给了浏览器几个cookies：CASPRIVACY、CASTGC和iPlanetDirectoryPro
2. 浏览器携带这些cookies，向新的网址`http://portal.chd.edu.cn/?ticket=ST-854426-Aye0eVjF4JmBvQyJa0le1563260380765-JRua-cas`发起GET请求，得到302的response，得到新的cookies：MOD_AUTH_CAS
3. 浏览器携带这些cookies，向新的网址`http://portal.chd.edu.cn/`发起GET请求，得到200的response，并给予新的cookies，也就是最重要的cookies：JSESSIONID



# 参考链接

- [使用cookies做PHP用户登录详解-CSDN](https://blog.csdn.net/awhip9/article/details/78007600)
- 如果导入本模块出了问题可以看这个：[Python 3.x可能是史上最详解的【导入（import）】-CSDN](https://blog.csdn.net/weixin_38256474/article/details/81228492)

