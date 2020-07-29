#-*- coding = utf-8 -*-
"""
@author: XRL
@software: PyCharm
@file: 51job_spider.py
@time: 2020/7/1 23:18
"""

import urllib.request,urllib.response
from bs4 import BeautifulSoup
import pymysql
import re
import sys


'''
51job搜索时完整链接
'''

originurl = 'https://search.51job.com/list/070200,000000,0000,00,9,99,Python,2,1.html' \
            '?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99' \
            '&ord_field=0&dibiaoid=0&line=&welfare='
# 数据库信息----------
host = '127.0.0.1'
port = 3306
user = 'XRL'
password = 'GTX1070xrl@123'
database = '51spider'
# -------------------
#要求爬取，南京-python-6-8k数据
def main():#除了页数，其他都确定了
    datalist = getData()
    saveData(datalist)



find_total_pagenum = re.compile(r'<span class="td">共(\d*)页，到第</span>',re.S)
find_job_name = re.compile(r'\
                    (.*?)                </a>')
find_job_link = re.compile(r'href="(.*?)" onmousedown')
find_co_name = re.compile(r'title="(.*)">')
find_co_link = re.compile(r'<span class="t2"><a href="(.*?)" target="_blank" title="')
find_job_place = re.compile(r'<span class="t3">(.*?)</span>')
find_job_salary = re.compile((r'<span class="t4">(.*?)</span>'))
find_release_time = re.compile(r'<span class="t5">(.*?)</span>')




def get_total_pagenum():
    origin_html = askURL(originurl)
    soup = BeautifulSoup(origin_html, 'html.parser')
    patt1 = soup.find_all('span',class_="td")
    patt1 = str(patt1)
    page_num = re.findall(find_total_pagenum,patt1)#输出了列表
    return page_num[0]

def test():
    origin_html = askURL(originurl)
    soup = BeautifulSoup(origin_html, 'html.parser')
    jobdata=[]
    datalist = []
    # -------------------
    baseurl = 'https://search.51job.com/list/070200,000000,0000,00,9,05'  # 截到发布时间 薪资6-8k
    cut1 = ',Python,2,'  # 截到页数选择前 +n.html
    cut2 = '.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99' \
           '&ord_field=0&dibiaoid=0&line=&welfare='
    # -------------------#这里可以用正则，刨除页数以外的字符串
    total_pagenum = int(get_total_pagenum())
    for i in range(1, total_pagenum + 1):
        makedurl = baseurl + cut1 + str(i) + cut2
        html = askURL(makedurl)
        soup = BeautifulSoup(html, 'html.parser')
        jobdata = []
        for i in soup.find_all('div',class_='el')[16:-1]:
            i = str(i)
            # print(i)
            data=[]
            job_name = re.findall(find_job_name, i)[0]  # 每个招聘信息中的职位名
            data.append(job_name)
            job_link = re.findall(find_job_link, i)
            if job_link !='':

                print(job_link)
    #         data.append(job_link)
    #         co_name = re.findall(find_co_name,i)[1]
    #         data.append(co_name)
    #         co_link = re.findall(find_co_link,i)[0]
    #         data.append(co_link)
    #         job_place = re.findall(find_job_place, i)[0]
    #         data.append(job_place)
    #         job_salary = re.findall(find_job_salary, i)[0]
    #         data.append(job_salary)
    #         release_time = re.findall(find_release_time, i)[0]
    #         data.append(release_time)
    #
    #         jobdata.append(data)
    # return jobdata



def getData():
    datalist = []
    #-------------------
    baseurl = 'https://search.51job.com/list/070200,000000,0000,00,9,05'  # 截到发布时间 薪资6-8k
    cut1 = ',Python,2,'  # 截到页数选择前 +n.html
    cut2 = '.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99' \
           '&ord_field=0&dibiaoid=0&line=&welfare='
    #-------------------#这里可以用正则，刨除页数以外的字符串
    total_pagenum = int(get_total_pagenum())
    for i in range(1,total_pagenum+1):
        makedurl = baseurl + cut1 + str(i)+ cut2
        html = askURL(makedurl)
        soup = BeautifulSoup(html, 'html.parser')
        for i in soup.find_all('div', class_='el')[16:]:
            i = str(i)
            data=[]
            job_name = re.findall(find_job_name, i)[0]#每个招聘信息中的职位名
            data.append(job_name)
            job_link = re.findall(find_job_link,i)[0]
            data.append(job_link)
            co_name = re.findall(find_co_name,i)[1]
            data.append(co_name)
            co_link = re.findall(find_co_link,i)[0]
            data.append(co_link)
            job_place = re.findall(find_job_place,i)[0]
            data.append(job_place)
            job_salary = re.findall(find_job_salary,i)[0]
            data.append(job_salary)
            release_time = re.findall(find_release_time,i)[0]
            data.append(release_time)

            datalist.append(data)
    return datalist

def askURL(url):
    head = {  # 模拟头部信息
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome / 78.0.3904.108 Safari / 537.36"
    }
    request =urllib.request.Request(url,headers=head)#?
    # print(request)
    html = ''
    try:
        response = urllib.request.urlopen(request)#?
        html = response.read().decode('gbk')
        # print(html)
        return html
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)

def testsave():
    initdb()
    conn = pymysql.connect(host=host,port=port,user=user,password=password,
                           database=database)
    cur = conn.cursor()
    datalist = getData()
    for data in datalist[0:1]:
        for index in range(len(data)):
            data[index] = '"'+data[index]+'"'
        sql='''
        insert into job_info(job_name,job_link,co_name,co_link,job_place,job_salary,release_time)
            values (%s)
        '''%",".join(data)
        print(",".join(data))
        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

def saveData(datalist):
    initdb()
    conn = pymysql.connect(host=host,port=port,user=user,password=password,
                           database=database)
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            data[index] = '"' + data[index] + '"'
        sql = '''
        insert into job_info(job_name,job_link,co_name,co_link,job_place,job_salary,release_time)
        values (%s)
        '''%",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

def initdb():

    '''
    t1 招聘职位名称
    t1 招聘职位对应的页面
    t2 招聘单位
    t2 招聘单位页面
    t3 工作地点
    t4 工资
    t5 发布时间
    '''
    sql = '''
    create table job_info
    (id int not null primary key AUTO_INCREMENT,
    job_name text not null ,
    job_link text not null ,
    co_name text not null ,
    co_link text not null ,
    job_place text not null ,
    job_salary text not null ,
    release_time text not null
    )
    '''
    conn = pymysql.connect(host = host,port = port,user = user,password = password,
                           database = database)
    cur = conn.cursor()
    print('数据库连接成功')
    try:
        cur.execute(sql)
        print('表创建成功')
    except pymysql.err.Error as e:
        print(e)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # print(test()[0])
    main()
    # print(getData()[0])
    # testsave()
    print('爬取成功')