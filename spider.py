# -*- codeing = utf-8 -*-
# @Time : 2021/3/31 23:17
# @Author : gzk
# @File : spider.py
# @Software : PyCharm


from bs4 import BeautifulSoup      #网页解析，获取数据
import re           #正则表达式，文字匹配
import urllib.request,urllib.error
import xlwt        #excel操作
import random
import pymysql.cursors


def main():

    ipList = ['27.43.188.200:9999', '58.253.154.234:9999', '60.187.113.250:9000', '182.34.26.240:9999']
    proxy_support = urllib.request.ProxyHandler({'http': random.choice(ipList)})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    baseurl = 'https://movie.douban.com/top250?start='

    # 获取网页
    dataList = getData(baseurl)
    # savePath = '豆瓣电影top.xlsx'

    # 保存数据
    saveDB(dataList)
    # saveData(dataList,savePath)


# 影片详情
findLink = re.compile(r'<a href="(.*?)">')   # 生成正则表达式对象，表示规则
# 影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # 忽略换行符
# 影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
# 找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 影片概况
findIng = re.compile(r'<span class="inq">(.*?)</span>')
# 影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 创建数据库
def initDB():
    # 创建连接
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='010426', db='guo', charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    try:
        cursor = conn.cursor()
        sql = '''create table movie (
                id int(11)  primary key ,
                info_link text ,
                pic_link text ,
                c_name varchar(60) ,
                o_name varchar(60) ,
                score float (5,1) ,
                rated int ,
                survey text ,
                information text
                )
        '''
        cursor.execute(sql)

    except Exception:
        print('default')
    finally:
        conn.close()
        cursor.close()


# 保存数据到数据库
def saveDB(dataList):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='010426', db='guo', charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    try:
        cursor = conn.cursor()
        for data in dataList:
            for index in range(len(data)):
                if index == 4 or index == 5:
                    continue
                data[index] = '"' + data[index] + '"'

            sql = '''insert into movie(
                       info_link,pic_link,c_name ,o_name, score, rated, survey, information ) 
                       value (%s)''' % ','.join(data)

            cursor.execute(sql)
        conn.commit()  # 提交数据要不然数据库不刷新
    except Exception:
        print('保存数据到库失败')
    finally:
        conn.close()
        cursor.close()


# 得到指定一个url的网页内容
def askUrl(url):
    # 用户代理表示豆瓣服务器我们是什么类型的机器
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    req = urllib.request.Request(url=url, headers=head)
    html = ''
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    return html


# 爬取网页
def getData(baseurl):
    dataList = []
    for i in range(0, 10):
        # 10页页面信息
        url = baseurl + str(i * 25)
        html = askUrl(url)
        # 逐一解析数据
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div', class_="item"):
            data = []     # 保存一部电影的所有信息
            item = str(item)
            link = re.findall(findLink, item)[0]      # 通过正则表达式查找
            data.append(link)     # 添加链接

            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)   # 添加图片

            title = re.findall(findTitle, item)
            if (len(title) == 2):
                ctitle = title[0]
                data.append(ctitle)
                otitle = title[1].replace('/', '')  # 去掉无关符号
                data.append(otitle)
            else:
                data.append(title[0])
                data.append(' ')       # 英文名留空

            Rating = re.findall(findRating, item)[0]
            data.append(Rating)      # 添加评分

            judge = re.findall(findJudge, item)[0]
            data.append(judge)    # 添加评价人数

            ing = re.findall(findIng, item)
            if len(ing) != 0:
                ing = ing[0].replace('。', '')   # 去掉句号
                data.append(ing)              # 添加概述
            else:
                data.append(" ")

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', ' ', bd)   # 去掉<br/>
            bd = re.sub('/', ' ', bd)
            data.append(bd.strip())   # 去掉前后空格
            dataList.append(data)
    return dataList


# 保存数据
def saveData(dataList,savePath):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('豆瓣电影top250', cell_overwrite_ok=True)  # 创建工作表
    # worksheet.write(0, 0, 'hello')  # 储存在内存中
    col =  ('排名','电影详情链接', '图片链接', '影片中文名', '影片外国名', '评分', '评分人数', '概况', '相关信息')
    for i in range(0,9):
        worksheet.write(0,i,col[i])
    for i in range(0,250):
        print('第%d条' % (i+1))    # 跟踪进程
        data = dataList[i]
        worksheet.write(i+1, 0, i+1)  # 储存在内存中
        for j in range(0,8):
            worksheet.write(i+1,j+1,data[j])
    workbook.save(savePath)  # 保存数据表


if __name__ == '__main__':
    main()
    # initDB()
    print('爬取完毕')
