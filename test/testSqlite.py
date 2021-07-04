# -*- codeing = utf-8 -*-
# @Time : 2021/4/2 12:24
# @Author : gzk
# @File : testSqlite.py
# @Software : PyCharm


import pymysql.cursors


# 创建连接
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='010426', db='girls', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

try:
    cursor = conn.cursor()
    sql = '''create table movie1 (
            id int(11)  primary key not null ,
            c_name varchar(10) ,
            o_name varchar(10) not null 
            )
    '''
    # sql = 'select * from boys'
    result = cursor.execute(sql)
    print(result)
    if result > 0:
        print('success')
    else :
        print('default')

    # result = cursor.fetchall()
    # for i in result:
    #     print(type(i))
    #     print(i)
except Exception:
    print('查询失败')



cursor.close()
conn.close()



