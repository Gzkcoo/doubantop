# -*- codeing = utf-8 -*-
# @Time : 2021/4/2 11:15
# @Author : gzk
# @File : testXls.py
# @Software : PyCharm

import xlwt

workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('sheet1')  #创建工作表
worksheet.write(0,0,'hello')     # 储存在内存中
workbook.save('student.xlsx')   # 保存数据表