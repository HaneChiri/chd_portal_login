'''
此模块是chd_portal_login.login模块的一个应用
'''
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取绝对路径
sys.path.append(BASE_DIR + '\\..')

import requests
from bs4 import BeautifulSoup
import logging
from chd_portal_login.login import *
import xlwt

def get_score(score_url,cookies,headers):
    '''
    获取各科成绩
    :param score_url: 成绩界面url
    :param cookies: 已登录的cookies
    :param headers: 请求头
    :return: [
        (表头1,表头2,...,表头n),
        (数据1,数据2,...,数据n),
        ...
        (数据1,数据2,...,数据n),
    ]
    '''
    response=requests.get(score_url,cookies=cookies,headers=headers)
    html=response.text
    soup=BeautifulSoup(html,'lxml')
    table=soup.find('div',{'class': 'grid'}).table
    # 获取表头
    thead=table.thead
    th_list=thead.tr.find_all('th')
    field=tuple([th.get_text() for th in th_list]) # 字段
    # 获取各科成绩
    tbody=table.tbody
    
    tr_list=tbody.find_all('tr')
    subjects=[field]
    for tr in tr_list:
        td_list=tr.find_all('td')
        subject=[td.get_text().strip() for td in td_list]
        subject=tuple(subject)
        subjects.append(subject)
        logging.debug(str(subject))
    return subjects
            
def save_score(file_name,score_table):
    '''
    将成绩表保存为xls文件
    :param file_name: 输出文件名
    :param score_table: 存储着成绩的二维可迭代对象
    '''
    workbook=xlwt.Workbook() # 创建工作簿
    score_sheet=workbook.add_sheet('成绩') # 创建工作表
    # 将成绩表写入
    for row in range(0,len(score_table)):
        for col in range(0,len(score_table[0])):
            score_sheet.write(row,col,score_table[row][col])
    # 保存
    logging.debug('保存成功')
    workbook.save(file_name)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    login_url = 'http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F'
    home_page_url = 'http://portal.chd.edu.cn/index.portal?.pn=p167'
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
    }
    cookies = login(login_url, headers, home_page_url,file_name='cookies')  #此函数最终返回一个cookies
    score_url='http://bkjw.chd.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR'
    get_score(score_url,cookies=cookies,headers=headers)
    score_table=get_score(score_url,cookies=cookies,headers=headers)
    save_score('score.xls',score_table)